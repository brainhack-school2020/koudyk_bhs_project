#! /usr/bin/env python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.colors import ListedColormap
from matplotlib.collections import LineCollection
from matplotlib.lines import Line2D
import math
import imageio

alpha = .15

# +
def make_segments(x, y):
    '''
    Create list of line segments from x and y coordinates, in the correct
    format for LineCollection:
    an array of the form   numlines x (points per line) x 2 (x and y) array
    '''

    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    return segments


def colorline(x, y, z=None, cmap=plt.get_cmap('copper'),
              norm=plt.Normalize(0.0, 1.0), linewidth=3, alpha=1.0):
    '''
    Plot a colored line with coordinates x and y
    Optionally specify colors in the array z
    Optionally specify a colormap, a norm function and a line width
    '''

    # Default colors equally spaced on [0,1]:
    if z is None:
        z = np.linspace(0.0, 1.0, len(x))

    # Special case if a single number:
    if not hasattr(z, "__iter__"):  # to check for numerical input -- hack
        z = np.array([z])

    z = np.asarray(z)

    segments = make_segments(x, y)
    lc = LineCollection(segments, array=z, cmap=cmap, norm=norm,
                        linewidth=linewidth, alpha=alpha)

    ax = plt.gca()
    ax.add_collection(lc)

    return lc


def circum_points(id_list, radius=10):
    '''
    Generate a dataframe with the coordinates of points along the
    circumference of a circle
    '''
    pi = math.pi
    N = len(id_list)
    pts = np.ones((N, 2))
    for n in range(0, N):
        pts[n, 0] = math.cos(2 * pi / N * n) * radius
        pts[n, 1] = math.sin(2 * pi / N * n) * radius

    df = pd.DataFrame(data=pts, columns=['x', 'y'], index=id_list)
    return df


def make_2color_cmap(color1, color2):
    '''
    Make a colormap that's a gradient between 2 colors
    '''
    rgb1 = colors.to_rgb(color1)
    rgb2 = colors.to_rgb(color2)
    N = 256
    vals = np.ones((N, 4))
    for comp in range(3):
        vals[:, comp] = np.linspace(rgb1[comp], rgb2[comp], N)
    cmap = ListedColormap(vals)
    return(cmap)


def make_cmps(constant_color, none_color, list_method_colors):
    '''
    Make all the colormaps needed here.
    '''
    cmaps = []
    rgbs_list = []
    for c in list_method_colors:
        cmaps.append(make_2color_cmap(c, constant_color))
        rgbs_list.append(colors.to_rgb(c))
    rgbs_list.append(colors.to_rgb(none_color))

    none_cmap = make_2color_cmap(none_color, constant_color)

    return none_cmap, cmaps, rgbs_list

def plot_methnet(data, coords, field_query, list_methods_queries, data_id,
                 gif_id, list_method_colors, constant_color, none_color):
    '''
    Plot the citation network, colored by methods mentioned.
    '''
    if constant_color == 'black':
        plt.style.use('dark_background')
    else:
        plt.style.use('seaborn-white')

    # make colormaps
    none_cmap, cmaps, rgbs_list = make_cmps(constant_color,
                                            none_color,
                                            list_method_colors)

    # plot ring of invisible dots (doesn't work if we dont; not sure why)
    plt.scatter(x=coords['x'], y=coords['y'], s=1,
                color=constant_color, alpha=0)

    n_none_found = 0
    for id_orig in data.index:

        # determine colormap based on software used
        none_found = True
        cmap = none_cmap
        for n, method in enumerate(list_methods_queries):
            if data.loc[id_orig, method] > 0:
                cmap = cmaps[n]
                color = rgbs_list[n]
                none_found = False

        # plot each reference as a line
        for id_ref in data.loc[id_orig, 'refs']:

            # location of citing paper
            x1, y1 = coords.loc[id_orig, 'x'], coords.loc[id_orig, 'y']

            # location of cited paper
            x2, y2 = coords.loc[id_ref, 'x'], coords.loc[id_ref, 'y']

            # create a list of coordinates for points on a line between
            # the 2 paper-points
            x = np.linspace(x1, x2, num=10)
            y = np.linspace(y1, y2, num=10)

            # make line between them
            colorline(x, y, cmap=cmap, linewidth=1, alpha=alpha)
            plt.axis('off')

        if not none_found:
            # make bigger colored dot for article in search results
            dot_color = np.expand_dims(np.array(color), axis=0)
            plt.scatter(x1, y1, s=10, c=dot_color, alpha=alpha)
        else:
            n_none_found = n_none_found + 1

    # create legend
    custom_lines = []
    for n, method in enumerate(list_methods_queries):  # + ['Other']):
        info = Line2D([0], [0], color=rgbs_list[n],
                      lw=2, label=method)
        custom_lines.append(info)
    legend = plt.legend(handles=custom_lines, fontsize='x-large',
                        loc='upper right', frameon=False,
                        title='Method keywords')
    plt.setp(legend.get_title(), fontsize='x-large')
    plt.tight_layout()

    plt.savefig(f'../images/visualization__{gif_id}.png')


def gif_of_methnet(data, field_query, list_methods_queries, data_id, gif_id,
                   list_method_colors, constant_color,
                   none_color, sort_by_year=False, shuffle=False,
                   figure_title=' '):
    '''
    '''
    # List all unique pmcids
    all_ids = data.index.to_list()
    for row in data['refs']:
        all_ids = all_ids + row
    all_ids = np.unique(all_ids)

    # sort by year if desired. This will make the points appear in order
    # around the circumference of the circle in the figure.
    if sort_by_year:
        data = data.sort_values('year')

    # shuffle all ids (search results & references) around the edge of the
    # circle in the figure
    if shuffle:
        np.random.seed(seed=39838475)
        np.random.shuffle(all_ids)

    # Make dataframe with x-y coordinates of each id on a circle
    coords = circum_points(id_list=all_ids, radius=20)

    # make a methnet figure per year
    years = np.unique(list(data['year']))
    years = years
    n_year = 0
    png_names = []
    all_years = range(np.min(years), np.max(years))
    for n_year, year in enumerate(all_years):
        print(f'Making png for year {n_year + 1} / {len(all_years)}', end='\r')

        # select portion of dataframe for all years up until given year
        if n_year == 0:
            d = data.loc[data['year'] == year]
        else:
            d = data.loc[data['year'] <= year]

        fig, ax = plt.subplots(figsize=(10, 10))
        plot_methnet(data=d, coords=coords,
                     field_query=field_query,
                     list_methods_queries=list_methods_queries,
                     data_id=data_id,
                     gif_id=gif_id,
                     list_method_colors=list_method_colors,
                     constant_color=constant_color,
                     none_color=none_color)

        title = (f'Citation network for\n{figure_title}\n\n{year}')
        plt.title(title, fontsize='xx-large', loc='center')
        plt.tight_layout()

        # save series of png files to be made into gif
        png_name = f'../images/images_for_gif/{gif_id}__{year}.png'
        plt.savefig(png_name)
        png_names.append(png_name)

    # make gif
    print('\n\nMaking GIF...')
    gif_name = f'../images/visualization__{gif_id}.gif'
    images = []
    repeat_last = 10
    for n, png_name in enumerate(png_names):
        image = imageio.imread(png_name)
        images.append(image)

        # repeat the last image so you see it for longer in the gif
        if n + 1 == len(png_names):
            for rep in range(repeat_last):
                images.append(image)
    imageio.mimsave(gif_name, images, duration=.5)
    print(f'GIF saved to\n{gif_name}')
    plt.close()
    return gif_name

# field_query = '"functional neuroimaging"[mesh] AND music[mesh]'
# list_methods_queries = ['spm', 'afni', 'nilearn', 'fsl']
# list_method_colors = ['green', 'dodgerblue', 'orange', 'red']
# data_id = "example"
# gif_id = "example"
#
# datafile = f'../data/pubmed_data__{data_id}.csv'
# data = pd.read_csv(datafile, converters={'refs': eval})
# data = data.set_index('pmcid', drop=True)
#
# gif_of_methnet(data, field_query, list_methods_queries, data_id, gif_id,
#                list_method_colors, constant_color='black',
#                none_color='black', sort_by_year=False, shuffle=False)
