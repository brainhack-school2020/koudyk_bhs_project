#! /usr/bin/env python3

import time
import requests
from lxml import etree
import IPython
import pprint
import json

# user input
field_query = 'fmri AND language'
methods_queries = ['spm', 'afni', 'nilearn', 'fsl']
email = 'kendra.oudyk@mail.mcgill.ca'
api_key_file = 'pubmed_api_key.txt'

# make dictionary to store results
data_fields = ['url', 'response', 'web_env', 'query_key', 'ids']
level_2_data = {key: [] for key in data_fields}
data = {key: level_2_data for key in methods_queries}

# prepare url
BASE_URL = ('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?')
DATABASE = 'pubmed'
TOOL = 'methnet'
api_key = open(api_key_file, 'r').read().strip()

try:
    for methods_query in methods_queries[0:1]:
        url = (f'{BASE_URL}db={DATABASE}&term={field_query}' +\
               f'+AND+{methods_query}&api_key={api_key}' +\
               f'&usehistory=y&email={email}&tool={TOOL}')
        url = url.replace('"', '%22')
        url = url.replace(' ', '+')

        # get data returned from the search, and the query key and web env
        # needed to re-use the search results from history
        response = requests.get(url)
        xml = response.content
        tree = etree.XML(xml)
        query_key = tree.find('QueryKey').text
        web_env = tree.find('WebEnv').text

        # populate data
        data[methods_query]['url'] = url
        data[methods_query]['response'] = response.text
        data[methods_query]['web_env'] = web_env
        data[methods_query]['query_key'] = query_key

        # get ids of papers that include the given methods-related keyword
        if int(tree.find('Count').text) > 0: # if there are any results
            for id_element in tree.iter('Id'):
                data[methods_query]['ids'].append(int(id_element.text))

        if len(methods_queries) > 10:
            time.sleep(.1) # pause so we don't exceed 10 requests per second
except:
    with open('pubmed_data_dumped_by_error.json', 'w') as json_file:
        json.dump(data, json_file)

with open('pubmed_data.json', 'w') as json_file:
    json.dump(data, json_file)
