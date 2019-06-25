#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse
from pathlib import Path

import numpy as np

"""
Util and module for generating reproducible integer data sets.
"""


def gen_normal_data(mu, sigma, size, seed=None):
    """Returns a random integer array, following a normal distribution."""
    np.random.seed(seed)

    data = np.random.normal(loc=mu, scale=sigma, size=size)
    data = np.rint(data)

    return data


def gen_lognormal_data(mu, sigma, size, seed=None):
    """Returns a random integer array, following a lognormal distribution."""
    np.random.seed(seed)

    data = np.random.lognormal(mean=mu, sigma=sigma, size=size)
    data = np.rint(data)

    return data


def save_data(data, out_file=None, gzip=False):
    """Saves an integer array as a .csv formatted file."""
    if out_file is None:
        np.savetxt(sys.stdout.buffer, data[None, :], fmt="%d", delimiter='\n')
    else:
        if gzip == True:
            out_file = out_file + ".gz"

        np.savetxt(out_file, data[None, :], fmt="%d", delimiter='\n')


def get_args():
    """Parse gen_dataset util arguments."""
    parser = argparse.ArgumentParser(description='''Generate an integer
    dataset following a given random distribution''')

    parser.add_argument(
        '--dist',
        choices=('normal', 'lognormal'),
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
        type=float,
        default=0,
        help='''mean of the distribution'''
    )
    parser.add_argument(
        '--sigma',
        type=float,
        default=1,
        help='''standard deviation of the distribution'''
    )
    parser.add_argument(
        '--gzip',
        action="store_true",
        default=False,
        help='''generate the output file as gzip (.gz)'''
    )
    parser.add_argument(
        '--outdir',
        default=None,
        help='''directory where output file is stored'''
    )
    parser.add_argument(
        '--pipe',
        action='store_true',
        default=False,
        help='''pipe output to stdout'''
    )

    return parser.parse_args()


def main():
    args = get_args()

    (mu, sigma, size, dist) = (args.mu, args.sigma, args.size, args.dist)
    if args.seed is None:
        seed = np.random.randint(0, 1000000)
    else:
        seed = args.seed

    if dist == 'normal':
        data = gen_normal_data(mu, sigma, size, seed=seed)
    elif dist == 'lognormal':
        data = gen_lognormal_data(mu, sigma, size, seed=seed)
    else:
        print("Unsupported distribution: {}.".format(args.dist))
        sys.exit()

    if args.pipe:
        out_file = None
    else:
        if args.outdir is None:
            path = Path.cwd()
        else:
            path = Path(args.outdir)
            if not path.is_dir():
                print("Invalid out-dir path: {}".format(path))
                sys.exit()

        file_tag = "{}_mu{}_s{}_n{}_seed{}".format(dist, mu, sigma, size, seed)
        file_tag = file_tag.replace('.', "_")
        path = Path(path, file_tag).with_suffix(".csv")

        out_file = str(path)

    save_data(data, out_file=out_file, gzip=args.gzip)


if __name__ == "__main__":
    main()
