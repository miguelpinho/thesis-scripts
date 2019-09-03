#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Sun Sep  1 14:14:46 2019

@author: miguelp
"""

from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


bench_size = ('normal', 'Normal size')
dist = ('logndist', 'Lognormal distribution')
fuse_dir = Path('./fuse')
nofuse_dir = Path('./no-fuse')
fu_used_file = 'simd_fu_used.csv'
fu_issued_file = 'simd_fu_issued.csv'
fu_extra_file = 'simd_fu_extra.csv'
width_class_file = 'width_class.csv'


# Original function by 'jrjc' user:
# https://stackoverflow.com/questions/22787209/how-to-have-clusters-of-stacked-bars-with-python-pandas
def plot_clustered_stacked(dfall, labels=None, title=None, yunit=None,
                           H="/", **kwargs):
    """Given a list of dataframes, with identical columns and index, create a clustered stacked bar plot. 
labels is a list of the names of the dataframe, used for the legend
title is a string for the title of the plot
H is the hatch used for identification of the different dataframe"""

    n_df = len(dfall)
    n_col = len(dfall[0].columns) 
    n_ind = len(dfall[0].index)
    axe = plt.subplot(111)

    for df in dfall : # for each data frame
        axe = df.plot(kind="bar",
                      linewidth=0,
                      stacked=True,
                      ax=axe,
                      legend=False,
                      grid=False,
                      **kwargs)  # make bar plots

    h,l = axe.get_legend_handles_labels() # get the handles we want to modify
    for i in range(0, n_df * n_col, n_col): # len(h) = n_col * n_df
        for j, pa in enumerate(h[i:i+n_col]):
            for rect in pa.patches: # for each index
                rect.set_x(rect.get_x() + 1 / float(n_df + 1) * i / float(n_col))
                rect.set_hatch(H * int(i / n_col)) #edited part     
                rect.set_width(1 / float(n_df + 1))

    axe.set_xticks((np.arange(0, 2 * n_ind, 2) + 1 / float(n_df + 1)) / 2.)
    axe.set_xticklabels(df.index, rotation = 0)
    if title is not None:
        axe.set_title(title)
    if yunit is not None:
        vals = axe.get_yticks()
        axe.set_yticklabels(['{}{}'.format(v, yunit) for v in vals])

    # Add invisible data to add another legend
    n=[]        
    for i in range(n_df):
        n.append(axe.bar(0, 0, color="gray", hatch=H * i))

    l1 = axe.legend(h[:n_col], l[:n_col], loc=[1.01, 0.5])
    if labels is not None:
        l2 = plt.legend(n, labels, loc=[1.01, 0.1]) 
    axe.add_artist(l1)
    return axe


def get_norm_stats(file, filter_out=None, drop_cols=None,
                   drop_empty_cols=False, unit=None):
    df = pd.read_csv(file)
    
    if filter_out is not None:
        df = df[df['benchmark'].str.contains(filter_out)]
    
    df['benchmark'] = df['benchmark'].map(lambda x: x.split('_')[0])
    df = df.set_index('benchmark')
    
    df = df.div(df.sum(axis=1), axis=0) * 100.0
    if drop_cols is not None:
        df = df.drop(columns=drop_cols)
    if drop_empty_cols:
        df = df.loc[:, (df != 0).any(axis=0)]
    if unit is not None:
        cols = df.columns.values.tolist()
        cols = [('{} {}' if (c is '1') else '{} {}s').format(c, unit) 
                for c in cols]
        df.columns = cols
    
    return df


def plot_comparison_stacked(dfall, labels=None, yunit=None,
                            label_anchor=None):
    
    n_df = len(dfall)
    
    fig, axes = plt.subplots(nrows=1, ncols=n_df, sharey=True)
    for i in range(n_df):
        dfall[i].plot(kind='bar', stacked=True, ax = axes[i], legend=False,
                      title=(None if (labels is None) else labels[i]))
    
    if yunit is not None:
        vals = axes[0].get_yticks()
        axes[0].set_yticklabels(['{}{}'.format(v, yunit) for v in vals])

    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, bbox_to_anchor=label_anchor, loc='center')
    plt.subplots_adjust(left=0.07, right=0.93, wspace=0.1)

    return (fig, axes)    


flag_zero = True

df_used_fuse = get_norm_stats(fuse_dir / fu_used_file,
                              filter_out=dist[0],
                              drop_cols=['0'], unit='FU')
df_used_nofuse = get_norm_stats(nofuse_dir / fu_used_file,
                                filter_out=dist[0],
                                drop_cols=['0'], unit='FU')

#print(df_used_fuse)
#print(df_used_nofuse)

ax_used = plot_clustered_stacked([df_used_fuse, df_used_nofuse],
                                  ['fuse', 'no fuse'],
                                  yunit='%', H='///')
plt.savefig('fig/simd_fu_used_{}_{}.png'.format(bench_size[0], dist[0]),
            bbox_inches='tight', format='png', dpi=300)

plot_comparison_stacked([df_used_fuse, df_used_nofuse], 
                        labels=['With Fuse', 'Without Fuse'],
                        yunit='%', label_anchor=(1.07,0.6))
plt.savefig('fig/simd_fu_used_{}_{}.pdf'.format(bench_size[0], dist[0]),
            bbox_inches='tight', format='pdf')


df_issued_fuse = get_norm_stats(fuse_dir / fu_issued_file,
                                filter_out=dist[0],
                                drop_cols=['0'],
                                drop_empty_cols=True,
                                unit='inst')
df_issued_nofuse = get_norm_stats(nofuse_dir / fu_issued_file,
                                  filter_out=dist[0],
                                  drop_cols=['0'],
                                  drop_empty_cols=True,
                                  unit='inst')

plot_comparison_stacked([df_issued_fuse, df_issued_nofuse],
                        labels=['With Fuse', 'Without Fuse'],
                        yunit='%', label_anchor=(1.07,0.6))
plt.savefig('fig/simd_fu_issued_{}_{}.pdf'.format(bench_size[0], dist[0]),
            bbox_inches='tight', format='pdf')

df_extra_fuse = get_norm_stats(fuse_dir / fu_extra_file,
                               filter_out=dist[0],
                               drop_cols=['0'],
                               drop_empty_cols=True,
                               unit='inst')
plot_comparison_stacked([df_issued_fuse, df_extra_fuse],
                        labels=['Total issued instructions',
                                'Fused instructions'],
                        yunit='%', label_anchor=(1.07,0.6))
plt.savefig('fig/simd_fu_issued_extra_{}_{}.pdf'.format(bench_size[0], dist[0]),
            bbox_inches='tight', format='pdf')

df_width_class = get_norm_stats(fuse_dir / width_class_file,
                                filter_out=dist[0],
                                drop_cols=['NoInfo','SimdNoInfo',
                                           'SimdNoPacking'])
plot_comparison_stacked([df_width_class],
                        yunit='%', label_anchor=(1.07,0.6))
