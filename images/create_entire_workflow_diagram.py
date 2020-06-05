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


###########################################
dot.edge('store', 'pubmed')
############################################
col = 'white'
dot.node('pubmed', label='All data')
dot.node('ydata', label='Select data\nup until given year')
dot.node('ring', label='Make x-y coordinates for a circle\nwith a point for each ID')
dot.node('line', ('For each search result,'
         '\ndraw lines between the SR-ID and its ref-IDs,'
         '\ncolored by the method mentioned'), color=col)
dot.node('cmaps', label='Make a colormap\n for each methods\nkeyword')
dot.node('pickc', label=('For each search result,'
         '\nChoose a colormap\n based on method mentioned'), color=col)
dot.node('fig', label='Save image for given year')
dot.node('gif', label='Make gif out of yearly images')

dot.edge('pubmed', 'ydata')
dot.edge('pubmed', 'ring', label='IDs of\nsearch results')
dot.edge('pubmed', 'ring', label='IDs of\nreferences')
dot.edge('cmaps', 'pickc', label='List of\ncolormaps')
dot.edge('ring', 'line', label='Coordinates')

with dot.subgraph(name='cluster_1') as d:
    d.attr(style='filled', color='lightgrey')
    d.attr(label='For each year', labeljust='l')
    d.edge('ydata', 'pickc', label='Counts of\nmethods keywords')
    d.edge('pickc', 'line', label='Colormap', color=col)
    d.edge('line', 'fig')

dot.edge('fig', 'gif')
############################
dot.render('./diagram_entire_workflow.gv', view=True)  # doctest: +SKIP
'diagram_entire_workflow.gv.png'
