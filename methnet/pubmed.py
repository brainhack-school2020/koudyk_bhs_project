#! /usr/bin/env python3

import pprint
import requests
from lxml import etree

# user input
field_query = 'fmri AND language'
methods_queries = ['spm', 'afni', 'nilearn'] # THIS WORKS
#methods_queries = ['spm', 'afni', 'nilearn', 'fsl'] # THIS DOESN'T WORK

# make dictionaries to store results
ids = {key: [] for key in methods_queries}
urls = {key: [] for key in methods_queries}

# prepare url
BASE_URL = ('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed')
field_query = field_query.replace(' ', '+')
for methods_query in methods_queries:
    url = (f'{BASE_URL}&term={field_query}+AND+{methods_query}&usehistory=y')
    urls[methods_query] = url

    # get ids of papers that include the given methods-related keyword
    response = requests.get(url)
    xml = response.content
    tree = etree.XML(xml)
    if int(tree.find('Count').text) > 0: # if there are any results
        for id_element in tree.iter('Id'):
            ids[methods_query].append(int(id_element.text))

pprint.pprint(urls)
pprint.pprint(ids)
