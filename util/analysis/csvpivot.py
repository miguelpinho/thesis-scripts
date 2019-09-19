#!/usr/bin/env python3

import sys
import numpy as np
import pandas as pd
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('col_name')
args = parser.parse_args()

coln = args.col_name
df = pd.read_csv(sys.stdin, header=None,
                 names=[coln, 'param', 'value'],
                 dtype={coln: np.str, 'param': np.str, 'value': np.str})

df = df.pivot(index=coln, columns='param', values='value')

df.to_csv(sys.stdout)
