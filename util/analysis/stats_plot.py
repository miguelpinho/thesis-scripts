#!/usr/bin/env python3

import sys
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

"""
Util for plotting gem5 statistics histograms.
"""


def get_args():
    """Return parsed args for op_classes util."""
    parser = argparse.ArgumentParser(
        description='''Analyse operation class stats'''
    )

    parser.add_argument(
        'in_file',
        help='''Input .csv file'''
    )
    parser.add_argument(
        'out_file',
        help='''Output .pdf file'''
    )
    parser.add_argument(
        '--stat',
        default="stat",
        help='''The stat being plotted'''
    )
    parser.add_argument(
        '--title',
        default="Plot Title",
        help='''Plot title'''
    )
    parser.add_argument(
        '--x-axis',
        default="x-axis label",
        help='''x-axis label'''
    )

    return parser.parse_args()


def main():
    args = get_args()

    path_in = Path(args.in_file)
    if not path_in.is_file():
        print('Invalid input path: {}.'.format(args.in_file))
        sys.exit()

    df = pd.read_csv(path_in)
    df = df.transpose()
    df[0] = df[0] / df[0].sum() * 100.0
    df.columns = [args.stat]
    df.index = df.index.astype('uint64')
    df = df.sort_index()
    ax = df.plot.bar(rot=0)
    ax.set(xlabel=args.x_axis, ylabel='Percentage of Clock Cycles [%]',
           title=args.title)
    plt.savefig(args.out_file, bbox_inches='tight')


if __name__ == "__main__":
    main()
