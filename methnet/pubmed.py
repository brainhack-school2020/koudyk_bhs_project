#! /usr/bin/env python3

import time
import requests
from lxml import etree
import json
import traceback
import pandas as pd
import IPython
import numpy as np

# user input
FIELD_QUERY = 'fmri AND language'
METHODS_QUERIES = ['spm', 'afni', 'nilearn', 'fsl']
EMAIL = 'kendra.oudyk@mail.mcgill.ca'
API_KEY_FILE = 'pubmed_api_key.txt'
YEARS = range(2016, 2019)

# more constants for URL
BASE_URL = ('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/')
TOOL = 'methnet'
DATABASE = 'pubmed'
# ELINK_LINKNAME = 'pmc_pmc_cites' # give PMCID
# ELINK_LINKNAME = 'pmc_refs_pubmed' # give PMCID
ELINK_LINKNAME = 'pubmed_pubmed_refs'  # give PMID
MAX_N_RESULTS = 100000
try:
    # if there's an API key provided, we can make 10 requests/sec, if not, 3
    API_KEY = open(API_KEY_FILE, 'r').read().strip()
    MAX_REQUESTS_PER_SEC = 11
except Exception:
    API_KEY = ['']  # this will go into the URL but will be ignored by the API
    MAX_REQUESTS_PER_SEC = 3

# make pandas dataframe to store results
columns = (['pmid', 'date', 'title', 'journal', 'refs'] + METHODS_QUERIES +
           ['esearch_url', 'esummary_url', 'elink_url'])
data = pd.DataFrame(columns=columns)
data = data.set_index('pmid', drop=True)


def build_esearch_url(methods_query):
    '''
    This function builds a esearch URL witht the given methods query.
    '''
    url = (f'{BASE_URL}esearch.fcgi?&db={DATABASE}&retmax={MAX_N_RESULTS}'
           f'&api_key={API_KEY}&email={EMAIL}&tool={TOOL}'
           f'&term={FIELD_QUERY}+AND+{methods_query}&usehistory=y')
    url = url.replace('"', '%22').replace(' ', '+').replace('()', '').\
          replace(')', '')
    return(url)


def build_elink_url(id):
    '''
    Returns an e-link URL for the ID for a paper.
    '''
    url = (f'{BASE_URL}elink.fcgi?&dbfrom={DATABASE}'
           f'&api_key={API_KEY}&email={EMAIL}&tool={TOOL}'
           f'&linkname={ELINK_LINKNAME}&id={id}')
    return url


def build_esummary_url_from_history(tree):
    '''
    This function builds a history url from the search results of a previous
    search.
    '''
    query_key = tree.find('QueryKey').text
    web_env = tree.find('WebEnv').text
    url = (f'{BASE_URL}esummary.fcgi?&db=pubmed&retmax={MAX_N_RESULTS}'
           f'&api_key={API_KEY}&email={EMAIL}&tool={TOOL}'
           f'&WebEnv={web_env}&query_key={query_key}')
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


try:
    for method in METHODS_QUERIES:
        esearch_url = build_esearch_url(method)

        # get response from URL in an XML tree format
        response = requests.get(esearch_url)
        tree = etree.XML(response.content)

        # get ids of papers that include the given methods-related keyword
        if int(tree.find('Count').text) > MAX_N_RESULTS:
            print(f'Warning: More than the max. number of results allowed per'
                  ' page; only the first {MAX_N_RESULTS} will be considered')
        if int(tree.find('Count').text) > 0:  # if there are any results
            esearch_ids = get_ids(tree)
        else:
            esearch_ids = []

        # get esummary results so we can look for the publication date later
        esummary_url = build_esummary_url_from_history(tree) + '&retmode=json'
        response = requests.get(esummary_url)
        esummary_json = response.json()

        # add new row in the data dataframe, one for each ID found
        data_method = pd.DataFrame(columns=columns)
        data_method['pmid'] = esearch_ids
        data_method = data_method.set_index('pmid', drop=True)
        data.append(data_method)

        space_searches(n_searches=len(METHODS_QUERIES))

        for n, esr_id in enumerate(esearch_ids):
            print('Methods query: %s, looking for date and refs for ID %d / %d'
                  % (method, n + 1, len(esearch_ids)), end='\r')

            # get the date, title, and journal for each paper
            date = esummary_json['result'][str(esr_id)]['pubdate']
            title = esummary_json['result'][str(esr_id)]['title']
            journal = esummary_json['result'][str(esr_id)]['fulljournalname']

            # get the ids of papers cited by each paper
            elink_url = build_elink_url(esr_id)
            response = requests.get(elink_url)
            elink_tree = etree.XML(response.content)
            elink_ids = get_ids(elink_tree)

            data.loc[esr_id, 'esearch_url'] = esearch_url
            data.loc[esr_id, 'esummary_url'] = esummary_url
            data.loc[esr_id, 'elink_url'] = elink_url
            data.loc[esr_id, method] = 1
            data.loc[esr_id, 'refs'] = elink_ids
            data.loc[esr_id, 'date'] = date
            data.loc[esr_id, 'title'] = title
            data.loc[esr_id, 'journal'] = journal

            space_searches(n_searches=len(esearch_ids))
        print('\n')

    # convert the dates given by pubmed to datetime
    data['date'] = pubmed_date_to_datetime(data['date'])

    # convert the methods columns to boolean
    data[METHODS_QUERIES] = data[METHODS_QUERIES].fillna(0)
    data[METHODS_QUERIES] = data[METHODS_QUERIES].astype(bool)

# save the data if there's an error so we can debug
except Exception as err:
    traceback.print_tb(err.__traceback__)
    print(err)
    with open('response_dumped_by_error.json', 'w') as json_file:
        json.dump(response.text, json_file)

# save all the data
data.to_csv('pubmed_data.csv')

# make matrix of references
print('\nConverting citation data to a matrix. This may take a while')

# list all unique pmids
ids = data.index.to_list()
for row in data['refs']:
    ids = ids + row
ids = np.unique(ids)

# make an empty adjacency matrix
mat = pd.DataFrame(columns=ids, index=[i for i in ids]).fillna(0)
mat.index = mat.index.rename('pmid')

# set to 1 when a pubmed ID
for n, pmid in enumerate(data.index):
    print('ID %d / %d' %(n + 1, len(data)), end='\r')
    for refid in data.loc[pmid]['refs']:
        mat.loc[pmid, refid] = 1
print('\n')

# save the matrix
mat.to_csv('pubmed_citation_matrix.csv')
