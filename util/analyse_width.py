#!/usr/bin/env python3

import sys
import argparse
import numpy as np
from pathlib import Path

"""
Util and module for analysing the width distribution of a data set.
"""


def get_signed_width(val):
    """Return the signed bit-width of an integer value."""
    val = int(val)
    if val < 0:
        return val.bit_length()
    else:
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
    path = Path(file)
    if not path.is_file():
        print('Invalid file path: {}'.format(path))
        sys.exit()

    return np.genfromtxt(str(path), dtype=int)


def get_args():
    """Parse analyse_width util arguments."""
    parser = argparse.ArgumentParser(description='''Analyse the width
    distribution of an integer data set''')

    parser.add_argument(
        '--bits',
        type=int,
        default=32,
        help='''maximum width of the integer values'''
    )
    parser.add_argument(
        '--width-def',
        choices=('signed', 'unsigned'),
        default='signed',
        help='''how the width is calculated'''
    )
    parser.add_argument(
        'file',
        help='''csv file with integer data set'''
    )

    return parser.parse_args()


def main():
    args = get_args()

    data = read_data(args.file)

    width = get_data_width(data, width_def=args.width_def)

    print(width)


if __name__ == "__main__":
    main()
