#! /usr/bin/env python3

# +
import visualizations as vis
import pubmed as pubmed
import os
import pandas as pd

def get_data(field_query,
             list_methods_queries,
             data_id,
             save_data=True):
    '''

    '''
    datafile = f'../data/pubmed_data__{data_id}.csv'
    if os.path.exists(datafile):
        print(f'Data has already been downloaded to\n{datafile}'
              '\n\nLoading data\n')
        data = pd.read_csv(datafile, converters={'refs': eval})
        data = data.set_index('pmcid', drop=True)
    else:
        print('Downloading data\n')
        data = pubmed.make_data(field_query, list_methods_queries, data_id,
                save_data=True)
    return data


def get_methnet(field_query,
            list_methods_queries,
            data_id,
            gif_id,
            list_method_colors,
            constant_color='black',
            none_color='black',
            sort_by_year=True,
            figure_title=' '):
    '''

    '''
    data = get_data(field_query=field_query,
                    list_methods_queries=list_methods_queries,
                    data_id=data_id,
                    save_data=True)

    gif_path = f'../images/visualization__{gif_id}.gif'
    png_path = gif_path[:-3] + 'png'
    if os.path.exists(gif_path):
        print(f'Figure has already been made:\n{gif_path}')
    else:
        print('\nMaking figure\n')
        gif_path = vis.gif_of_methnet(data=data,
                                    field_query=field_query,
                                    list_methods_queries=list_methods_queries,
                                    data_id=data_id,
                                    gif_id=gif_id,
                                    list_method_colors=list_method_colors,
                                    constant_color=constant_color,
                                    none_color=constant_color,
                                    sort_by_year=sort_by_year,
                                    figure_title=figure_title)
    return gif_path, png_path, data
