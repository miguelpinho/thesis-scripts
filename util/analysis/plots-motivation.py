# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt


fu_integerNN = Path('stats/no-fuse-4FU/integerNN/fu.csv.gz')
fu_streamvbyte = Path('stats/no-fuse-4FU/streamvbyte/fu.csv.gz')

clk_cycle = 500
sl_integerNN = slice(5000, 18000)
#sl_streamvbyte = slice(1250000, 1300000)
sl_streamvbyte = slice(3250000, 3300000)

pdf_integerNN = Path('fig/simd_fu_trace_integerNN.pdf')
pdf_streamvbyte = Path('fig/simd_fu_trace_streamvbyte.pdf')


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
    axes[1].set_ylabel('SIMD width required')
    axes[1].set_yticks(128 * np.arange(5))
    axes[1].grid(axis='y', linestyle='--')
    axes[1].set_xlabel('Clock cycle')
    fig.align_ylabels(axes[:])
    
    fig.savefig(out_file, bbox_inches='tight')


plt_fu_trace(fu_integerNN, sl_integerNN, pdf_integerNN)
plt_fu_trace(fu_streamvbyte, sl_streamvbyte, pdf_streamvbyte)
