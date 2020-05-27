#! /usr/bin/env python3

# the goal for this script is to access the pubmed ids
import pathlib
import requests
import numpy as np
import pprint
import IPython
import xml.etree.ElementTree as ET

OUTPUT_DIR = pathlib.Path('results_pubmed')

# esearch url, to be formatted with search terms, etc.
url_base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
url_unformatted = url_base + 'esearch.fcgi?db={db}&term={query}&usehistory=y'
db = 'pubmed'

# define keywords to search for
ids = {'python': [],
       'matlab': []
}
for keyword in ids.keys():
    # assemble the esearch url for given keyword
    query_unformatted = 'functional+neuroimaging[mesh]+AND+{keyword}+AND+2016[pdat]' \
        + '+AND+pubmed+pmc+open+access[filter]' # for pubmed
        # + '+AND+open+access[filter]' # for pmc
    query = query_unformatted.format(keyword=keyword)
    esr_url = url_unformatted.format(db=db, query=query)
    print(esr_url, '\n')

    # get ids of papers that include the given keyword
    esr_response = requests.get(esr_url)
    esr_root = ET.fromstring(esr_response.text)
    idlist_parent = esr_root.find('IdList')
    for child in idlist_parent:
        ids[keyword].append(int(child.text))
