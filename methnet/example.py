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

# +
import methnet_master as methnet
from IPython.display import Image

field_query = ('"functional neuroimaging"[mesh] AND (fMRI[Title/Abstract] OR "functional magnetic resonance imaging"[Title/Abstract] OR "functional MRI"[Title/Abstract]) AND music[mesh]')
list_methods_queries = ['spm', 'afni', 'nilearn', 'fsl']
list_method_colors = ['green', 'dodgerblue', 'orange', 'red']
data_id = "example"
gif_id = "example"
figure_title = "Music fMRI"

gif_path, png_path, data = \
    methnet.get_methnet(field_query=field_query,
                   list_methods_queries=list_methods_queries,
                   data_id=data_id,
                   gif_id=gif_id,
                   list_method_colors=list_method_colors,
                   constant_color='black',
                   none_color='black',
                   sort_by_year=True,
                   figure_title=figure_title)

# if you're running this in a jupyter notebook,
# this line will show the gif inline
Image(gif_path)
