#! /usr/bin/env python3

import time
import requests
from lxml import etree
import IPython
import pprint

# user input
field_query = 'fmri AND language'
methods_queries = ['spm', 'afni', 'nilearn', 'fsl'] # THIS DOESN'T WORK
email = 'kendra.oudyk@mail.mcgill.ca'
api_key_file = 'pubmed_api_key.txt'

# make dictionaries to store results
ids = {key: [] for key in methods_queries}
urls = {key: [] for key in methods_queries}

# prepare url
BASE_URL = ('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?')
DATABASE = 'pubmed'
TOOL = 'methnet'
field_query = field_query.replace(' ', '+')
api_key = open(api_key_file, 'r').read().strip()


for methods_query in methods_queries:
    url = (f'{BASE_URL}db={DATABASE}&term={field_query}' +\
           f'+AND+{methods_query}&api_key={api_key}' +\
           f'&usehistory=y&email={email}&tool={TOOL}')
    urls[methods_query] = url

    # get data returned from the search, and the query key and web env needed
    # to re-use the search results from history
    response = requests.get(url)
    xml = response.content
    tree = etree.XML(xml)
    query_key = tree.find('QueryKey').text
    web_env = tree.find('WebEnv').text

    # get ids of papers that include the given methods-related keyword
    if int(tree.find('Count').text) > 0: # if there are any results
        for id_element in tree.iter('Id'):
            ids[methods_query].append(int(id_element.text))

    if len(methods_queries) > 10:
        time.sleep(.1) # pause so we don't exceed 10 requests per second

pprint.pprint(urls)
pprint.pprint(ids)
