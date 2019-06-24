#!/usr/bin/env python3

import sys
import argparse
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from gen_dataset import save_data

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


def read_data(file):
    """Return data read from a .csv formatted file."""
    return np.genfromtxt(file, dtype=int)


def save_width_hist(data, file, bits=64, title=None):
    """Saves an integer width values array as a .pdf histogram figure."""
    plt.hist(data, bins=bits+1, range=(0, bits+1),
             density=True, facecolor='blue')

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
        default=False
    )
    parser.add_argument(
        '--hist',
        action='store_true',
        default=False
    )

    return parser.parse_args()


def main():
    args = get_args()

    in_path = Path(args.in_file)
    if not in_path.is_file():
        print('Invalid file path: {}'.format(args.in_file))
        sys.exit()

    if args.outdir is None:
        out_folder = Path.cwd()
    else:
        out_folder = Path(args.outdir)
        if not out_folder.is_dir():
            print('Invalid outdir specified: {}'.format(args.outdir))
            sys.exit()

    data = read_data(str(in_path))
    width = get_data_width(data, width_def=args.width_def)

    tag = "_{}_width".format(args.width_def)

    if args.csv == True:
        csv_path = Path(out_folder, in_path.stem + tag).with_suffix('.csv')
        save_data(width, file=str(csv_path))

    if args.hist == True:
        hist_path = Path(out_folder, in_path.stem + tag).with_suffix('.pdf')
        save_width_hist(width, hist_path, bits=args.bits)

    print(width)


if __name__ == "__main__":
    main()
