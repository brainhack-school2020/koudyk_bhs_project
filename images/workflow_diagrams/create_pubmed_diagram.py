from graphviz import Digraph

dot = Digraph(comment='Pipeline', format='png')

dot.node('input', 'User input')
dot.node('esearch', 'Esearch e-utility\nto look for search results')
dot.node('idconv', 'Idconv\nto convert IDs to allow searches\nin PubMed and PubMed Central')
dot.node('efetch', 'Efetch e-utility')
dot.node('search', 'xpath\nto search for info')
dot.node('count', 'str.count()\nto count mentions of keywords')
dot.node('elink', 'Elink e-utility\nto get references\nfor each PMID')
dot.node('store', 'Pandas dataframe\n to store data for given PMCID')

dot.edge('input', 'esearch', label=' PubMed\nquery')
dot.edge('esearch', 'idconv', label=' PMIDs')
dot.edge('idconv', 'efetch', label=' PMCID')
dot.edge('input', 'count', label=f' methods\n keywords')
dot.edge('idconv', 'elink', label='PMCID')


with dot.subgraph(name='cluster_0') as c:
    c.attr(style='filled', color='lightgrey')
    #c.node_attr.update(style='filled', color='white')
    c.edge('efetch', 'search', label='article\nin XML')
    c.edge('search', 'store', label='title, journal,\ndate, PMID',)

    c.edge('efetch', 'count', label='article\n in XML')
    c.edge('count', 'store', label=' counts of\nmethod\n keywords')

    c.edge('elink', 'store', label='PMIDs\nof refs')
    c.attr(label='For each PMCID', labeljust='l')

dot.render('./diagram_pubmed.gv', view=True)  # doctest: +SKIP
'diagram_pubmed.gv.png'
