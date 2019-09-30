# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import altair as alt
import matplotlib.pyplot as plt


fu_integerNN = Path('stats/no-fuse-4FU/integerNN/fu.csv.gz')
fu_streamvbyte = Path('stats/no-fuse-4FU/streamvbyte/fu.csv.gz')
width_integerNN = Path('stats/no-fuse-4FU/integerNN/statVectorInstTotalWidthByClass.csv')
width_streamvbyte = Path('stats/no-fuse-4FU/streamvbyte/statVectorInstTotalWidthByClass.csv')


clk_cycle = 500
sl_integerNN = slice(5000, 18000)
sl_streamvbyte = slice(3250000, 3300000)

total_bit = 128
step_bit = 32

pdf_integerNN = Path('fig/simd_fu_trace_integerNN.pdf')
pdf_streamvbyte = Path('fig/simd_fu_trace_streamvbyte.pdf')
svg_width = Path('fig/simd_width_ranges.svg')

width_classes = {'SimdPackingAlu': 'SimdAlu', 'SimdPackingMult': 'SimdMult'}


def plt_fu_trace(in_file, sl, out_file):
    df = pd.read_csv(in_file, header=0, usecols=['tick', 'fu used', 'width'],
                     skiprows=range(1, sl.start+1), nrows=sl.stop-sl.start,
                     compression='gzip')

    df['cycle'] = (df['tick'] - df['tick'].iloc[0]) / clk_cycle
    df['cycle'] = df['cycle'].astype(np.int64)
    df = df.set_index('cycle')

    print('Trace has {} cycles'.format(
          df.tail(1).index[0]))

    fig, axes = plt.subplots(nrows=2, sharex=True)
    df['fu used'].plot(ax=axes[0])
    df['width'].plot(ax=axes[1])
    axes[0].set_ylabel('SIMD FUs used')
    axes[0].set_yticks(np.arange(5))
    axes[0].grid(axis='y', linestyle='--')
    axes[1].set_ylabel('SIMD width required [bits]')
    axes[1].set_yticks(128 * np.arange(5))
    axes[1].grid(axis='y', linestyle='--')
    axes[1].set_xlabel('Clock cycle')
    fig.align_ylabels(axes[:])

    fig.savefig(out_file, bbox_inches='tight')


def get_width_data(in_file):
    df = pd.read_csv(in_file, header=0, index_col='class')
    df = df.rename(columns=lambda c: np.int64(c.split('-')[0]))
    df = df.sort_index(axis="columns")

    df_rg = pd.DataFrame(index=df.index)
    for a in range(0, total_bit, step_bit):
        b = a + step_bit
        df_rg[b] = df.loc[:,a+1:b].sum(axis="columns")

    df_rg = df_rg / df_rg.sum().sum() * 100.0
    df_rg = df_rg.loc[list(width_classes)]
    df_rg = df_rg.rename(index=width_classes)
    return df_rg


def plot_width_data(in_files, labels, out_file):
    n = len(in_files)
    dfs = [get_width_data(f) for f in in_files]

    for df, lbl in zip(dfs, labels):
        df['benchmark'] = lbl

    dfs = pd.concat(dfs, sort=True)
    dfs = dfs.reset_index().melt(id_vars=['benchmark', 'class'])

    chart = alt.Chart(dfs).mark_bar().encode(
            x=alt.X('class:N', title=None),
            y=alt.Y('sum(value):Q',
                    axis=alt.Axis(grid=False,
                                  title='Fraction of issued instructions [%]')),
            column=alt.Column('benchmark:N', title='Benchmark'),
            color=alt.Color('variable:N',
                            scale=alt.Scale(
                                scheme='yellowgreenblue'),
                            legend=alt.Legend(title="Width ranges"))
            ).configure_view(strokeOpacity=0)

    chart.save(out_file, webdriver='firefox')


#plt_fu_trace(fu_integerNN, sl_integerNN, pdf_integerNN)
#plt_fu_trace(fu_streamvbyte, sl_streamvbyte, pdf_streamvbyte)

plot_width_data([width_integerNN, width_streamvbyte],
                ['integerNN', 'streamvbyte'],
                svg_width)









