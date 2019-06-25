#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

from gen_data import save_data

"""
Util and module for analysing the width distribution of a data set.
"""


def get_signed_width(val):
    """Return the signed bit-width of an integer value."""
    val = int(val)
    if val < 0:
        val = -val - 1

    return val.bit_length() + 1


def get_unsigned_width(val):
    """Return the unsigned bit-width of an integer value."""
    val = int(val)
    return val.bit_length()


def get_data_width(data, width_def='signed'):
    option = width_def.lower().strip()

    if option == 'signed':
        width_func = get_signed_width
    elif option == 'unsigned':
        width_func = get_unsigned_width
    else:
        print("Invalid width definition: {}".format(width_def))

    return np.array(list(map(width_func, data)))


def read_data(in_file=None):
    """Return data read from a .csv formatted file."""
    if in_file is None:
        return np.loadtxt(sys.stdin, dtype=int)

    return np.loadtxt(in_file, dtype=int)


def save_width_hist(data, file, bits=64, cumulative=False, title=None):
    """Saves an integer width values array as a .pdf histogram figure."""
    plt.hist(data, bins=bits+1, range=(0, bits+1),
             density=True, cumulative=cumulative, facecolor='blue')

    plt.xlabel('Bit-width [bits]')
    plt.ylabel('Fraction')
    if title is None:
        plt.title('Bit-width Histogram')
    else:
        plt.title(title)

    plt.savefig(file)


def get_args():
    """Parse analyse_width util arguments."""
    parser = argparse.ArgumentParser(description='''Analyse the width
    distribution of an integer data set''')

    parser.add_argument(
        'in_file',
        nargs='?',
        default=None,
        help='''csv file with integer data set'''
    )
    parser.add_argument(
        '--bits',
        type=int,
        default=64,
        help='''maximum width of the integer values'''
    )
    parser.add_argument(
        '--width-def',
        choices=('signed', 'unsigned'),
        default='signed',
        help='''how the width is calculated'''
    )
    parser.add_argument(
        '--outdir',
        default=None,
        help='''dir for storing output files'''
    )
    parser.add_argument(
        '--csv',
        action='store_true',
        default=False,
        help='''output data width as .csv file'''
    )
    parser.add_argument(
        '--hist',
        action='store_true',
        default=False,
        help='''output width histogram as .pdf figure file'''
    )
    parser.add_argument(
        '--cumulative',
        action='store_true',
        default=False,
        help='''output cumulative width histogram as .pdf figure file'''
    )

    return parser.parse_args()


def main():
    args = get_args()

    if args.in_file is None:
        in_stem = 'pipe'
        in_file = None
    else:
        in_path = Path(args.in_file)
        if not in_path.is_file():
            print('Invalid file path: {}'.format(args.in_file))
            sys.exit()
        in_stem = in_path.stem
        in_file = str(in_path)

    if args.outdir is None:
        out_folder = Path.cwd()
    else:
        out_folder = Path(args.outdir)
        if not out_folder.is_dir():
            print('Invalid outdir specified: {}'.format(args.outdir))
            sys.exit()

    data = read_data(in_file=in_file)
    width = get_data_width(data, width_def=args.width_def)

    tag = "_{}_width".format(args.width_def)

    if args.csv == True:
        csv_path = Path(out_folder, in_stem + tag).with_suffix('.csv')
        save_data(width, out_file=str(csv_path))

    if args.hist == True:
        hist_path = Path(out_folder, in_stem + tag +
                         "_hist").with_suffix('.pdf')
        save_width_hist(width, hist_path, bits=args.bits)

    if args.cumulative == True:
        cumulative_path = Path(out_folder, in_stem + tag +
                               "_cumulative").with_suffix('.pdf')
        save_width_hist(width, cumulative_path,
                        bits=args.bits, cumulative=True,
                        title='Cumulative Bit-width Histogram')


if __name__ == "__main__":
    main()
