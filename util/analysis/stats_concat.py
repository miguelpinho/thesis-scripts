#!/usr/bin/env python3

import sys
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

"""
Util to join several benchmarks .csv files in only one table.
"""


def get_args():
    """Return parsed args for op_classes util."""
    parser = argparse.ArgumentParser(
        description='''Analyse operation class stats'''
    )

    parser.add_argument(
        'dir',
        help='''Benchmark dir'''
    )
    parser.add_argument(
        'stat',
        help='''Stat of the .csv files to join'''
    )
    parser.add_argument(
        '--out-file',
        default=None,
        help='''Output joined .csv file'''
    )

    return parser.parse_args()


def main():
    args = get_args()

    dir_root = Path(args.dir)
    if not dir_root.is_dir():
        print('Invalid dir path {}.'.format(args.dir))
        sys.exit()

    files = sorted(dir_root.glob('**/{}'.format(args.stat)))

    df_concat = []
    for f in files:
        bench = f.parent.stem
        df_bench = pd.read_csv(f)

        df_bench['benchmark'] = bench
        df_concat.append(df_bench)

    df = pd.concat(df_concat)

    if args.out_file is None:
        out_file = dir_root / '{}'.format(args.stat)
    else:
        out_file = Path(args.out_file)
    df.to_csv(out_file, index=False)


if __name__ == "__main__":
    main()
