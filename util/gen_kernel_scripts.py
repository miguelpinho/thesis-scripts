#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse
import random
from pathlib import Path

"""
Util for generating the thesis-kernels sim-sripts.
"""


# scripts template
script_fmt = ('#!/bin/bash               \n'
              '                          \n'
              'BENCH_DIR="{}"            \n'
              'KERNEL_DIR="$BENCH_DIR/{}"\n'
              'cd $KERNEL_DIR            \n'
              'pwd                       \n'
              'ls                        \n'
              '                          \n'
              '{} {}                     \n'
              'm5 exit                     ')

# algebra kernels (blas, level)
algebra_kernels = [
    ('asum', 1),
    ('axpy', 1),
    ('dot', 1),
    ('iamax', 1),
    ('sqnrm2', 1),
    ('amax_cols', 2),
    ('asum_cols', 2),
    ('gemv', 2),
    ('ger', 2),
    ('sqnrm2_cols', 2),
    ('gemm', 3)
]

# workload sizes
workload_sizes = {
    'tiny': ['1098304', '1024 1024', '256 256 256'],
    'small': ['4194304', '2048 2048', '512 512 512'],
    'normal': ['16777216', '4096 4096', '1048 1048 1048'],
    'large': ['67108864', '8192 8192', '2048 2048 2048']
}

# data distributions
data_dist = {
    'ndist': [
        'normal_mu0_0_s10000_0_n100000000_seed901738.csv',
    ],
    'logndist': [
        'lognormal_mu5_0_s3_5_n100000000_seed152168.csv',
    ]
}


def get_args():
    """Return parsed args for gen_kernel_scripts util."""
    parser = argparse.ArgumentParser(
        description='''Generate the simulation scripts for thesis-kernels benchmarks'''
    )

    parser.add_argument(
        'outdir',
        help='''dir for the generated scripts'''
    )

    return parser.parse_args()


def print_script(path, prg, prg_args, bench_path='/root/benchmarks',
                 kernel_dir='thesis-kernels'):
    """Prints the run script file for the given kernel."""
    with open(path, 'w') as outfile:
        outfile.write(script_fmt.format(
            bench_path, kernel_dir, prg, ' '.join(prg_args)))


def main():
    args = get_args()

    outdir = Path(args.outdir)
    if not outdir.is_dir():
        print('Invalid outdir: {}'.format(args.outdir))
        sys.exit()

    for tag, size in workload_sizes.items():
        benchmarks = {'1': [], '2': [], '3': []}

        for kernel in algebra_kernels:
            for d, data in data_dist.items():
                blas = kernel[0]
                level = kernel[1]

                bench = '{}_{}_{}.sh'.format(blas, tag, d)
                path = outdir / bench
                benchmarks[str(level)].append(bench)
                prg = './build/{}'.format(blas)
                prg_args = []
                prg_args.append(size[level-1])
                prg_args.append("./data/{}".format(random.choice(data)))

                print_script(path, prg, prg_args)

        for level, b in benchmarks.items():
            bench_file = outdir / '{}_level{}.txt'.format(tag, level)
            with open(bench_file, 'w') as outfile:
                outfile.write('\n'.join(b))


if __name__ == "__main__":
    main()
