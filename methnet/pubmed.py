#! /usr/bin/env python3

# the goal for this script is to access the pubmed ids
import pathlib
import requests
import numpy as np
import pprint
import IPython
from lxml import etree
import xml.etree.ElementTree as ET

OUTPUT_DIR = pathlib.Path('results_pubmed')

# assemble the esearch url
url_base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
url_unformatted = url_base + 'esearch.fcgi?db={db}&term={query}&usehistory=y'
db = 'pmc'
ids = {'matlab': [],
        'python': []
}
for keyword in ids.keys():
    # assemble url for given keyword
    query_unformatted = 'music+AND+fMRI+AND+{keyword}+AND+2016[pdat]' \
        + '+AND+open+access[filter]'
    query = query_unformatted.format(keyword=keyword)
    esr_url = url_unformatted.format(db=db, query=query)
    print(esr_url, '\n')

    # get ids
    esr_response = requests.get(esr_url)
    esr_root = ET.fromstring(esr_response.text)
    idlist_thing = esr_root.find('IdList')
    for child in idlist_thing:
        ids[keyword].append(int(child.text))

IPython.embed()
