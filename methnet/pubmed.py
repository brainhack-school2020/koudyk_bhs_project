#! /usr/bin/env python3

# the goal for this script is to access the pubmed data
import pathlib
import requests
import numpy as np
import pprint
import IPython
from lxml import etree
import xml.etree.ElementTree as ET

OUTPUT_DIR = pathlib.Path('results_pubmed')

# assemble the esearch url
# esearch gets the IDs for papers matching the search results
url_base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
url_unformatted = url_base + 'esearch.fcgi?db={db}&term={query}&usehistory=y'
db = 'pubmed'
query = 'music[mesh]+AND+functional+neuroimaging[mesh]+AND+fMRI+AND+2016[pdat]' \
    + '+AND+pubmed+pmc+open+access[filter]'
esr_url = url_unformatted.format(db=db, query=query)
print(esr_url, '\n')

# get the esearch results
esr_response = requests.get(esr_url)
esr_root = ET.fromstring(esr_response.text)
query_key = esr_root.find('QueryKey').text
web_env = esr_root.find('WebEnv').text

# assemble the esummary url
esm_url_unformatted = url_base + 'esummary.fcgi?db={db}&query_key={query_key}&WebEnv={web_env}'
esm_url = esm_url_unformatted.format(db=db, query_key=query_key, web_env=web_env)
print(esm_url, '\n')

esm_response = requests.get(esm_url)

# assemble the efetch url
esf_url_unformatted = url_base + 'efetch.fcgi?db={db}&query_key={query_key}&WebEnv={web_env}' \
+ '&retmode=xml'
esf_url = esf_url_unformatted.format(db=db, query_key=query_key, web_env=web_env)
print(esf_url, '\n')

esf_response = requests.get(esf_url)

#IPython.embed()
