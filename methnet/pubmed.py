#! /usr/bin/env python3

import time
import requests
from lxml import etree
import json
import copy
import traceback
import pandas as pd
import IPython

# user input
FIELD_QUERY = 'fmri AND language'
METHODS_QUERIES = ['spm', 'afni', 'nilearn', 'fsl']
EMAIL = 'kendra.oudyk@mail.mcgill.ca'
API_KEY_FILE = 'pubmed_api_key.txt'

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
    MAX_REQUESTS_PER_SEC = 10
except Exception:
    API_KEY = ['']  # this will go into the URL but will be ignored by the API
    MAX_REQUESTS_PER_SEC = 3

# make pandas dataframe to store results
columns = (['pmid', 'date'] + METHODS_QUERIES + ['refs',
        'esearch_url', 'ehistory_url', 'elink_url'])
data = pd.DataFrame(columns=columns)
data = data.set_index('pmid', drop=True)
IPython.embed()

def build_esearch_url(methods_query):
    '''
    This function builds a esearch URL witht the given methods query.
    '''
    url = (f'{BASE_URL}esearch.fcgi?&db={DATABASE}&retmax={MAX_N_RESULTS}'
           f'&api_key={API_KEY}&email={EMAIL}&tool={TOOL}'
           f'&term={FIELD_QUERY}+AND+{methods_query}')  # '&usehistory=y')
    url = url.replace('"', '%22').replace(' ', '+')
    return(url)


def build_elink_url(id):
    '''
    Returns an e-link URL for the ID for a paper.
    '''
    url = (f'{BASE_URL}elink.fcgi?&dbfrom={DATABASE}'
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

        # add new row in the data dataframe, one for each ID found
        data_method = pd.DataFrame(columns=columns)
        data_method['pmid'] = esearch_ids
        data_method = data_method.set_index('pmid', drop=True)
        data.append(data_method)

        # pause if needed so we don't exceed the max number requests per second
        space_searches(n_searches=len(METHODS_QUERIES))

        for n, esearch_id in enumerate(esearch_ids):
            print('Methods query: %s, looking for refs for ID %d / %d'
                  % (method, n + 1, len(esearch_ids)), end='\r')
            elink_url = build_elink_url(esearch_id)
            response = requests.get(elink_url)
            elink_tree = etree.XML(response.content)
            elink_ids = get_ids(elink_tree)

            data.loc[esearch_id, 'esearch_url'] = esearch_url
            data.loc[esearch_id, 'elink_url'] = elink_url
            data.loc[esearch_id, method] = 1
            data.loc[esearch_id, 'refs'] = elink_ids

            space_searches(n_searches=len(esearch_ids))
        print('\n')

# save the data if there's an error so we can debug
except Exception as err:
    traceback.print_tb(err.__traceback__)
    print(err)
    with open('response_dumped_by_error.json', 'w') as json_file:
        json.dump(response.text, json_file)

# save the data at the end if there's no error
data.to_csv('pubmed_data.csv')

# def build_esearch_history_url(tree):
#     '''
#     This function builds a history url from the search results of a previous
#     search.
#     '''
#     query_key = tree.find('QueryKey').text
#     web_env = tree.find('WebEnv').text
#     url = (f'{BASE_URL}esearch.fcgi?&db=pubmed&retmax={MAX_N_RESULTS}' +\
#            f'&api_key={API_KEY}&email={EMAIL}&tool={TOOL}' +\
#            f'&WebEnv={web_env}&query_key={query_key}')
#     return url
