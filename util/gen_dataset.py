#!/usr/bin/env python3

import sys
import argparse
import numpy as np
import random
from pathlib import Path

"""
Util and module for generating reproducible integer data sets.
"""


def gen_normal_data(mu, sigma, size, seed=None):
    np.random.seed(seed)

    data = np.random.normal(loc=mu, scale=sigma, size=size)
    data = np.rint(data)

    return data


def save_data(data, file=None, gzip=False):
    if gzip == True:
        file = file + ".gz"

    np.savetxt(file, data[None, :], fmt="%d", delimiter=',\n')


def get_args():
    """Parse gen_dataset arguments."""
    parser = argparse.ArgumentParser(description='''Generate integer dataset
    following a given distribution''')

    parser.add_argument(
        '--dist',
        choices=('normal'),
        default='normal',
        help='''distribution type'''
    )
    parser.add_argument(
        '-S',
        '--seed',
        type=int,
        default=None,
        help='''random seed'''
    )
    parser.add_argument(
        '-N',
        '--size',
        type=int,
        default=100,
        help='''number of samples for the generated data set'''
    )
    parser.add_argument(
        '--mu',
        type=int,
        default=0,
        help='''mean of the distribution'''
    )
    parser.add_argument(
        '--sigma',
        type=int,
        default=1,
        help='''standard deviation of the distribution'''
    )
    parser.add_argument(
        '-Z',
        '--gzip',
        action="store_true",
        default=False,
        help='''generate the output file as gzip (.gz)'''
    )
    parser.add_argument(
        'outdir',
        help='''directory where output file is stored'''
    )

    return parser.parse_args()


def main():
    args = get_args()

    (mu, sigma, size) = (args.mu, args.sigma, args.size)
    if args.seed is None:
        seed = random.randint(0, 1000000)
    else:
        seed = args.seed

    data = gen_normal_data(mu, sigma, size, seed=seed)

    path = Path(args.outdir)
    if not path.is_dir():
        print("Invalid out-dir path: {}".format(path))
        sys.exit()

    file_tag = "normal_mu{}_s{}_n{}_seed{}.out".format(mu, sigma, size, seed)
    path = path / file_tag

    save_data(data, file=str(path), gzip=args.gzip)


if __name__ == "__main__":
    main()
