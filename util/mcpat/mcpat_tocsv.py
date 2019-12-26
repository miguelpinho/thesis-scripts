#!/usr/bin/env python3

"""
Simple util for parsing mcpat output into a .csv table.
"""


import sys
from pathlib import Path
import pandas as pd
import argparse


components = {
    'processor': slice(11,19),
    'core': slice(40, 46),
    'fetch': slice(48, 54),
    'rename': slice(137, 143),
    'load store': slice(177, 183),
    'mmu': slice(209, 214),
    'execute': slice(232, 237),
    'register file': slice(239, 245),
    'scheduler': slice(263, 269),
    'int alu': slice(295, 301),
    'fp/simd alu': slice(303, 309),
    'int mul/div': slice(311, 317),
    'result bus': slice(319, 325),
    'bus': slice(336, 342)
}


def get_args():
    """Parse mcpat_tocsv arguments."""
    parser = argparse.ArgumentParser(description='Parse mcpat output to csv.')
    
    parser.add_argument(
        'in_file',
        nargs='?',
        default=None,
        help='''input file'''
    )
    parser.add_argument(
        '-o',
        '--out_file',
        default = None,
        help='''csv output file'''
    )

    return parser.parse_args()


def parse_mcpat(args):
    """Parse mcpat output to csv."""
    if args.in_file is None:
        in_file = sys.stdin
    else:
        in_file = Path(args.in_file)
        if not in_file.is_file():
            print("Invalid input path: {}".format(in_file))
            sys.exit()
        in_file = open(in_file, 'r')

    lines = in_file.readlines()
    
    # Parse power stats to a dataframe.
    df = {}
    for key, val in components.items():
        param = {}
        for l in lines[val]:
            name = l.split('=')[0].strip()
            value, unit = l.split('=')[1].strip().split(' ')
            
            param['{} [{}]'.format(name, unit)] = value
        s = pd.Series(param, name='Value')
        s.index.name = 'Parameter'
        s.reset_index()
        df[key] = s
    df = pd.DataFrame.from_dict(df, orient='index')
    df.index.name = 'Component'
    df = df.sort_index(axis=1)

    # Save dataframe to csv file.
    if args.out_file is None:
        out_file = sys.stdout
    else:
        out_file = Path(args.out_file)

    df.to_csv(out_file)
    
    if args.in_file is not None:
        in_file.close()


def main():
    args = get_args()
    parse_mcpat(args)


if __name__ == "__main__":
    main()
