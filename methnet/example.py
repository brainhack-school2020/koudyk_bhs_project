# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.3.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# # Example of how to use methnet

# There are 3 main stages involved in this package:
# 1. A user inputs a [PubMed query](https://pubmed.ncbi.nlm.nih.gov/advanced/) to get papers and a list of methods-related keywords to search for (e.g., software names);
# 2. The package gets the data using the [NCBI Entrez Programming E-utilities](https://www.ncbi.nlm.nih.gov/books/NBK25497/) to find papers matching the query, list their references, and access the full text so the package can count instances of the keywords in each paper; and
# 3. The the package creates a [gif visualization](https://github.com/brainhack-school2020/koudyk_bhs_project/blob/master/images/visualization__example.gif) of the data.
#
# The details of what this package does can be seen in this [workflow diagram](https://github.com/brainhack-school2020/koudyk_bhs_project/blob/master/images/workflow_diagrams/diagram_entire_workflow.gv.png).

import methnet_master as methnet
from IPython.display import Image

# ## How to use this package
#
# ### 1. Define a field query
# You need to define a PubMed query to find papers for the field they're interested in. It might be helpful to build a query using the [PubMed website's advanced search function](https://pubmed.ncbi.nlm.nih.gov/advanced/) to get the syntax right. 
#
# Note that there are additional filters used in this package, so you might see more results on the website than you'll get from this package.

field_query = ('"functional neuroimaging"[mesh] AND (fMRI[Title/Abstract] OR "functional magnetic resonance imaging"[Title/Abstract] OR "functional MRI"[Title/Abstract]) AND music[mesh]')

# ### 2. Define a list of methods-related keywords
# Next, list some methods keywords to search for in the papers found (e.g., names of software). In this package, we just search for whether each keyword was mentioned anywhere in the text, and we do not search for synonyms. This means that the keyword should be specific.
# - Bad example: "data" (too generic)
# - Good example: "SPSS" (specific)
#

list_methods_queries = ['spm', 'afni', 'nilearn', 'fsl']

# ### 3. Choose a color for each keyword
# You need to make a list of colors that's the same length as the list of methods-related keywords.

list_method_colors = ['green', 'dodgerblue', 'orange', 'red']

# ### 4. Define the identifiers for the data and figure
# You can choose identifiers that will be appended to the name of the datafile and the gif. 
#
# If there's a data file with the data ID, then that data will be loaded. If you want to change your queries for the download, be sure to change the data ID. 
#
# Likewise, if there's a figure with the figure ID, then the figure will not be created again. So if you want to change something about the figure (e.g., the colors), then you should change the gif ID. 

data_id = "example"
gif_id = "example"

# ### 5. Choose a title for the figure
# Choose a title for the figure that summarizes your field query. 

figure_title = "Music fMRI"

# ### 6. Change the parameters of the figure (optional)
# You can change these parameters if you want. They'll change what the figure looks like. 
#
# Each paper has lines going from itself to the papers that it cites around the circle. 
#
# The **constant_color** is the color of the end of the lines near the references. If this color is black, the background will be black; if not, it will be white.
#
# The **none_color** is the color of those papers in which none of the methods-related keywords are mentioned. I recommend that this be the same color as the constant_color. 
#
# If **sort_by_year** is True, papers will appear around the  circumference of the citation circle in approximate chronological order. If false, they'll be placed randomly.

constant_color = 'black'
none_color = 'black' 
sort_by_year = True

# ## Then run this cell
# You shouldn't need to change any of this code. 

# +
gif_path, png_path, data = \
    methnet.get_methnet(field_query=field_query,
                   list_methods_queries=list_methods_queries,
                   data_id=data_id,
                   gif_id=gif_id,
                   list_method_colors=list_method_colors,
                   constant_color=constant_color,
                   none_color=none_color,
                   sort_by_year=sort_by_year,
                   figure_title=figure_title)

# if you're running this in a jupyter notebook,
# this line will show the gif inline
Image(gif_path)
