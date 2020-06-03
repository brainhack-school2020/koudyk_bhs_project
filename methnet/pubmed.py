#! /usr/bin/env python3

import time
import requests
from lxml import etree
import json
import traceback
import pandas as pd
import IPython
import numpy as np
import re

print_urls = True  # I set this to true when debugging

# user input
FIELD_QUERY = '"functional neuroimaging"[mesh] AND music[mesh]'
METHODS_QUERIES = ['spm', 'afni', 'nilearn', 'fsl']
EMAIL = 'kendra.oudyk@mail.mcgill.ca'
API_KEY_FILE = 'pubmed_api_key.txt'
YEARS = range(2016, 2019)

# more constants for URL
BASE_URL = ('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/')
TOOL = 'methnet'
ESEARCH_DB = 'pubmed'
ELINK_DB = 'pmc'
ELINK_LINKNAME = 'pmc_pmc_cites' # give PMCID
# ELINK_LINKNAME = 'pmc_refs_pubmed' # give PMCID
#ELINK_LINKNAME = 'pubmed_pubmed_refs'  # give PMID
MAX_N_RESULTS = 100000
try:
    # if there's an API key provided, we can make 10 requests/sec, if not, 3
    API_KEY = open(API_KEY_FILE, 'r').read().strip()
    MAX_REQUESTS_PER_SEC = 11
except Exception:
    API_KEY = ['']  # this will go into the URL but will be ignored by the API
    MAX_REQUESTS_PER_SEC = 3

# make pandas dataframe to store results
columns = (['pmcid', 'pmid', 'month', 'year', 'title', 'journal', 'refs'] +
           METHODS_QUERIES +
           ['esearch_url', 'efetch_url', 'elink_url'])
data = pd.DataFrame(columns=columns)
data = data.set_index('pmcid', drop=True)


def build_esearch_url():
    '''
    This function builds a esearch URL witht the given methods query.
    '''
    url = (f'{BASE_URL}esearch.fcgi?&db={ESEARCH_DB}&retmax={MAX_N_RESULTS}'
           f'&api_key={API_KEY}&email={EMAIL}&tool={TOOL}&usehistory=y'
           f'&term={FIELD_QUERY}+AND+pubmed+pmc+open+access[filter]')
           # f'&term={FIELD_QUERY}+AND+{methods_query}&usehistory=y')
    url = url.replace('"', '%22').replace(' ', '+').replace('()', '').\
              replace(')', '')
    return(url)

def build_efetch_url_from_history(pmcid, esearch_tree):
    query_key = esearch_tree.find('QueryKey').text
    web_env = esearch_tree.find('WebEnv').text
    efetch_url = (f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
                  f'efetch.fcgi?db=pmc&id={pmcid}'
                  f'&api_key={API_KEY}&email={EMAIL}&tool={TOOL}'
                  f'&WebEnv={web_env}&query_key={query_key}')
    return efetch_url


def build_elink_url(id):
    '''
    Returns an e-link URL for the ID for a paper.
    '''
    url = (f'{BASE_URL}elink.fcgi?&dbfrom={ELINK_DB}'
           f'&api_key={API_KEY}&email={EMAIL}&tool={TOOL}'
           f'&linkname={ELINK_LINKNAME}&id={id}')
    return url


def get_ids(tree):
    '''
    Get the list of IDs from an XML tree
    '''
    ids = []
    for id_element in tree.iter('Id'):
        ids.append(int(id_element.text))
    return ids


def space_searches(n_searches):
    '''
    Space out the searches in time so that we don't exceed the max. allowed
    per second. With the API, it is 10/sec; without it is 3/sec
    '''
    if n_searches > MAX_REQUESTS_PER_SEC:
        time.sleep(MAX_REQUESTS_PER_SEC/100)


def pubmed_date_to_datetime(df_date_column):
    '''
    Put the date into datetime format
    '''
    temp = (data['date'].str.replace('Summer', 'Jul').
            replace('Fall', 'Oct').replace('Autumn', 'Oct').
            replace('Winter', 'Jan').replace('Spring', 'May'))
    temp = temp.str[0:8]
    datetime_column = pd.to_datetime(temp, yearfirst=True)
    return datetime_column


def divide_list_into_chunks(my_list, chunk_len):
    for i in range(0, len(my_list), chunk_len):
        yield my_list[i:i + chunk_len]


def pmids_to_pmcids(pmid_list):
    pmcids = []
    urls = []
    before = '" pmcid="PMC'
    after = '" pmid="'
    # break list of ids into chunks of 200, since that is the limit for the api
    ids_in_chunks = list(divide_list_into_chunks(esearch_ids, 200))
    for chunk in ids_in_chunks:
        cnvrt_url = ('https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?'
                 f'api_key={API_KEY}&tool={TOOL}&email={EMAIL}&ids={chunk}').replace(' ', '').replace('[', '').replace(']', '')
        urls.append(cnvrt_url)
        if print_urls: print('PMID-PMCID URL: ', cnvrt_url, '\n')
        response = requests.get(cnvrt_url)
        resp_text = response.text
        starts = [m.start() for m in re.finditer(before, resp_text)]
        starts = [start + len(before) for start in starts]
        ends = [m.start() for m in re.finditer(after, resp_text)]
        for start, end in zip(starts, ends):
            pmcids.append(int(resp_text[start : end]))

        space_searches(n_searches=len(ids_in_chunks))
    return pmcids, urls


def get_method_data(pmcids, esearch_tree):
    '''
    Get the number of times each method is mentioned in each paper.
    '''
    method_data = np.zeros((len(pmcids), len(METHODS_QUERIES)))
    for n_id, pmcid in enumerate(pmcids):
        print(f'Getting data for ID {n_id} / {len(pmcids)}', end='\r')
        efetch_url = build_efetch_url_from_history(pmcid, esearch_tree)
        response = requests.get(efetch_url)
        resp_text = response.text.lower()

        for n_meth, method in enumerate(METHODS_QUERIES):
            method_data[n_id, n_meth] = resp_text.count(method)
    return method_data


def get_first_instance(tree, term):
    items = []
    for el in eft_tree.iter(term):
        items.append(el.text)
    return items[0]

try:
    # ESEARCH ##############################################################
    esearch_url = build_esearch_url()
    if print_urls: print('ESEARCH URL', esearch_url, '\n')

    # get response from URL in an XML tree format
    response = requests.get(esearch_url)
    esearch_tree = etree.XML(response.content)

    # get ids of papers that include the given methods-related keyword
    if int(esearch_tree.find('Count').text) > MAX_N_RESULTS:
        print(f'Warning: More than the max. number of results allowed per'
              ' page; only the first {MAX_N_RESULTS} will be considered')
    if int(esearch_tree.find('Count').text) > 0:  # if there are any results
        esearch_ids = get_ids(esearch_tree)
    else:
        esearch_ids = []
        print('No search results :\'(' )

    # convert the pubmed ids from the search results to pmc ids, so that we
    # can access the full text with efetch
    pmcids, cnvrt_urls = pmids_to_pmcids(esearch_ids)
    #pmcids = pmcids[:10]  # limit number while figuring out code

    # add new row in the data dataframe, one for each ID found
    data_method = pd.DataFrame(columns=columns)
    data_method['pmcid'] = pmcids
    data_method = data_method.set_index('pmcid', drop=True)
    data.append(data_method)

    # get data for each paper
    for n_id, pmcid in enumerate(pmcids):
        print(f'Getting data for ID {n_id} / {len(pmcids)}', end='\r')

        # EFETCH ##############################################################
        # use efetch to get the full text
        efetch_url = build_efetch_url_from_history(pmcid, esearch_tree)
        if print_urls: print('EFETCH URL', efetch_url, '\n')
        response = requests.get(efetch_url)
        resp_text = response.text.lower()
        eft_tree = etree.XML(response.content)

        title = get_first_instance(eft_tree, 'article-title')
        journal = get_first_instance(eft_tree, 'journal-title')
        month = get_first_instance(eft_tree, 'month')
        year = get_first_instance(eft_tree, 'year')

        # get the counts of the number of times each method was mentioned
        for n_meth, method in enumerate(METHODS_QUERIES):
            data.loc[pmcid, method] = resp_text.count(method)

        # ELINK ##############################################################
        # get the ids of papers cited by each paper
        elink_url = build_elink_url(pmcid)
        if print_urls: print('ELINK URL', elink_url, '\n')
        response = requests.get(elink_url)
        elink_tree = etree.XML(response.content)
        elink_ids = get_ids(elink_tree)

        data.loc[pmcid, 'pmid'] = esearch_ids[n_id]
        data.loc[pmcid, 'refs'] = elink_ids
        data.loc[pmcid, 'month'] = month
        data.loc[pmcid, 'year'] = year
        data.loc[pmcid, 'title'] = title
        data.loc[pmcid, 'journal'] = journal
        data.loc[pmcid, 'esearch_url'] = esearch_url
        data.loc[pmcid, 'efetch_url'] = efetch_url
        data.loc[pmcid, 'elink_url'] = elink_url
        data.loc[pmcid, 'pm_pmc_cnvrt_urls'] = cnvrt_urls

        space_searches(n_searches=len(pmcids))

    print('\n')

# save the data if there's an error so we can debug
except Exception as err:
    traceback.print_tb(err.__traceback__)
    print(err)
    with open('response_dumped_by_error.json', 'w') as json_file:
        json.dump(response.text, json_file)

# save all the data
data.to_csv('pubmed_data.csv')

# # make matrix of references
# print('\nConverting citation data to a matrix. This may take a while')
#
# # list all unique pmids
# ids = data.index.to_list()
# for row in data['refs']:
#     ids = ids + row
# ids = np.unique(ids)
#
# # make an empty adjacency matrix
# mat = pd.DataFrame(columns=ids, index=[i for i in ids]).fillna(0)
# mat.index = mat.index.rename('pmid')
#
# # set to 1 when a pubmed ID
# for n, pmid in enumerate(data.index):
#     print('ID %d / %d' % (n + 1, len(data)), end='\r')
#     for refid in data.loc[pmid]['refs']:
#         mat.loc[pmid, refid] = 1
# print('\n')
#
# # save the matrix
# mat.to_csv('pubmed_citation_matrix.csv')
