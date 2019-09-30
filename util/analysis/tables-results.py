#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
import pandas as pd

folders = ['./stats/no-fuse-4FU', './stats/fuse-4FU', './stats/no-fuse-2FU',
           './stats/fuse-2FU', './stats/no-fuse-1FU', './stats/fuse-1FU']
labels  = ['NF.4', 'F.4', 'NF.2', 'F.2', 'NF.1', 'F.1']

timing_files = [Path(f) / 'time.csv' for f in folders]
timing_dfs = [pd.read_csv(f, header=0, index_col=['benchmark'])
                for f in timing_files]

dfs = timing_dfs
for idx, lbl in enumerate(labels):
    dfs[idx] = dfs[idx].rename(columns={'clk cycles': lbl})

df = pd.concat(dfs, axis='columns', sort=False)
df.index = df.index.map(lambda x: x.split('_')[0])
df.to_csv('tables/timing_kernels.csv')

df_norm = df.div(df['NF.4'], axis='index').round(decimals=3)
df_norm.to_csv('tables/norm_timing_kernels.csv')
