#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

"""
Util for analysing operation class stats.
"""

map_groups = {
    'No_OpClass': 'NoOp', 'IntAlu': 'IntAlu', 'IntMult': 'IntMult', 'IntDiv': 'IntDiv', 'FloatAdd': 'Float',
    'FloatCmp': 'Float', 'FloatCvt': 'Float', 'FloatMult': 'Float', 'FloatMultAcc': 'Float', 'FloatDiv': 'Float',
    'FloatMisc': 'Float', 'FloatSqrt': 'Float', 'SimdAdd': 'SimdAdd', 'SimdAddAcc': 'SimdAdd', 'SimdAlu': 'SimdAlu',
    'SimdCmp': 'SimdAlu', 'SimdCvt': 'SimdAlu', 'SimdMisc': 'SimdAlu', 'SimdMult': 'SimdMult', 'SimdMultAcc': 'SimdMult',
    'SimdShift': 'SimdAlu', 'SimdShiftAcc': 'SimdAlu', 'SimdSqrt': 'SimdSqrt', 'SimdFloatAdd': 'SimdFloat',
    'SimdFloatAlu': 'SimdFloat', 'SimdFloatCmp': 'SimdFloat', 'SimdFloatCvt': 'SimdFloat', 'SimdFloatDiv': 'SimdFloat',
    'SimdFloatMisc': 'SimdFloat', 'SimdFloatMult': 'SimdFloat', 'SimdFloatMultAcc': 'SimdFloat',
    'SimdFloatSqrt': 'SimdFloat', 'SimdAes': 'SimdCrypto', 'SimdAesMix': 'SimdCrypto', 'SimdSha1Hash': 'SimdCrypto',
    'SimdSha1Hash2': 'SimdCrypto', 'SimdSha256Hash': 'SimdCrypto', 'SimdSha256Hash2': 'SimdCrypto',
    'SimdShaSigma2': 'SimdCrypto', 'SimdShaSigma3': 'SimdCrypto', 'MemRead': 'Mem', 'MemWrite': 'Mem',
    'FloatMemRead': 'Mem', 'FloatMemWrite': 'Mem', 'IprAccess': 'Mem', 'InstPrefetch': 'Mem'
}


def get_args():
    """Return parsed args for op_classes util."""
    parser = argparse.ArgumentParser(
        description='''Analyse operation class stats'''
    )

    parser.add_argument(
        'in_dir',
        help='''Input .csv file'''
    )
    parser.add_argument(
        '--out-file',
        default=None,
        help='''Output file'''
    )

    return parser.parse_args()


def get_op_hist(in_file):
    """Returns a dataframe with the operation classes histogram."""
    df = pd.read_csv(in_file, delimiter=',', encoding='utf-8-sig')

    df['OpGroup'] = df['OpClass'].map(map_groups)
    df = df.groupby('OpGroup').agg('sum')
    df['Fraction%'] = df['Count'] / df['Count'].sum() * 100.0

    return df


def main():
    args = get_args()

    path = Path(args.in_dir)
    if not path.is_dir():
        print('Invalid dir path: {}.'.format(args.in_dir))
        sys.exit()

    files = sorted(path.glob('*.csv'))

    hists = [get_op_hist(f).drop(columns=['Count']).set_axis(
        [f.stem], axis=1, inplace=False) for f in files]
    df = pd.concat(hists, axis=1)

    # drop op groups that do not appear
    df = df.loc[(df != 0).any(axis=1)]

    print(df)
    df.transpose().plot.bar(stacked=True)

    if args.out_file is None:
        out_file = Path().cwd() / 'op_hist.pdf'
    else:
        out_file = Path(args.out_file)

    plt.savefig(out_file, bbox_inches='tight')


if __name__ == "__main__":
    main()
