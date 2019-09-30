#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
import altair as alt
import pandas as pd


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


folders = ['./stats/no-fuse-4FU', './stats/fuse-4FU', './stats/no-fuse-2FU',
           './stats/fuse-2FU', './stats/no-fuse-1FU', './stats/fuse-1FU']
labels  = ['NF.4', 'F.4', 'NF.2', 'F.2', 'NF.1', 'F.1']
legends = ['No fuse, 4 FUs', 'Fuse, 4 FUs', 'No fuse, 2 FUs', 'Fuse, 2 FUs',
           'No fuse, 1 FU', 'No fuse, 1 FU']

fu_usage_files = [Path(f) / 'simd_fu_used.csv' for f in folders]
fu_usage_dfs = [get_norm_stats(f, unit='FU') for f in fu_usage_files]

dfs = fu_usage_dfs
for ind in range(len(dfs)):
    dfs[ind]['config'] = labels[ind] 
    dfs[ind] = dfs[ind].set_index(['config'], append=True)

dfs = pd.concat(dfs, sort=True).fillna(0)
dfs = dfs.reset_index().melt(id_vars=['benchmark', 'config'])

chart = alt.Chart(dfs).mark_bar().encode(
        x=alt.X('config:N', sort='descending', title=None),
        y=alt.Y('sum(value):Q',
                axis=alt.Axis(grid=False,
                              title='Fraction of cycles [%]'),
                scale=alt.Scale(domain=[0, 100])),
        column=alt.Column('benchmark:N', title='Benchmark'),
        color=alt.Color('variable:N',
                        scale=alt.Scale(
                            scheme='yellowgreenblue'),
                        legend=alt.Legend(title="Active SIMD FUs"))
        ).configure_view(strokeOpacity=0)

chart.save('fig/simd_usage.svg', webdriver='firefox')