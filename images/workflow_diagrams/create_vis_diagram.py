from graphviz import Digraph

dot = Digraph(comment='Visualization', format='png')


###################
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

##############


dot.render('./diagram_vis.gv', view=True)  # doctest: +SKIP
'diagram_vis.gv.png'
