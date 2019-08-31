#!/usr/bin/env python3

import sys
import numpy as np
import pandas as pd

df = pd.read_csv(sys.stdin, header=None,
                 names=['fu', 'param', 'value'],
                 dtype={'fu': np.str, 'param': np.str, 'value': np.str})

df = df.pivot(index='fu', columns='param', values='value')

df.to_csv(sys.stdout)
