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
    ('fft', 1),
    ('sqnrm2', 1),
    ('amax_cols', 2),
    ('asum_cols', 2),
    ('gemv', 2),
    ('ger', 2),
    ('sqnrm2_cols', 2),
    ('gemm', 3)
]

# algebra workload sizes
workload_sizes = {
    # 'tiny': ['1098304', '1024 1024', '256 256 256'],
    # 'small': ['4194304', '2048 2048', '512 512 512'],
    'normal': [['65536', '400'], ['2048 1024', '200'], ['1048 524 524', '5']],
    # 'large': ['67108864', '8192 8192', '2048 2048 2048']
}

# integer data distributions
data_dist = {
    '8bit': [
        "normal_mu0_0_s65_0_n17000000_seed112444.csv",
        "normal_mu0_0_s65_0_n17000000_seed358739.csv",
        "normal_mu0_0_s65_0_n17000000_seed485805.csv",
        "normal_mu0_0_s65_0_n17000000_seed611651.csv",
        "normal_mu0_0_s65_0_n17000000_seed803661.csv",
    ],
    '12bit': [
        "lognormal_mu4_0_s2_2_n17000000_seed125529.csv",
        "lognormal_mu4_0_s2_2_n17000000_seed161353.csv",
        "lognormal_mu4_0_s2_2_n17000000_seed395922.csv",
        "lognormal_mu4_0_s2_2_n17000000_seed50444.csv",
        "lognormal_mu4_0_s2_2_n17000000_seed853852.csv",
    ],
    '16bit': [
        "lognormal_mu5_0_s3_3_n17000000_seed283146.csv",
        "lognormal_mu5_0_s3_3_n17000000_seed289906.csv",
        "lognormal_mu5_0_s3_3_n17000000_seed339531.csv",
        "lognormal_mu5_0_s3_3_n17000000_seed534724.csv",
        "lognormal_mu5_0_s3_3_n17000000_seed950812.csv",
    ]
}

# image kernels
image_kernels = [
    "conv",
    "img_hist",
    "img_integral",
    "img_erode",
    "img_canny",
    "img_cartoon",
    "img_yuv444",
    "img_median",
    "img_scale"
]

# ppm image files
data_img = {
    "image1.ppm",
    "image2.ppm",
    "image3.ppm",
    "image4.ppm",
    "image5.ppm"
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

    # generate algebra scripts
    for tag, size in workload_sizes.items():
        benchmarks = {'1': [], '2': [], '3': []}

        for kernel in algebra_kernels:
            for d, data in data_dist.items():
                blas = kernel[0]
                level = kernel[1]

                for idx, data_file in enumerate(data):
                    bench = '{}_{}_{}_{}.sh'.format(blas, tag, d, idx)
                    path = outdir / bench
                    benchmarks[str(level)].append(bench)

                    prg = './build/{}'.format(blas)
                    prg_args = []
                    prg_args.append(size[level-1][0])
                    prg_args.append("./data/{}".format(data_file))
                    prg_args.append(size[level-1][1])

                    print_script(path, prg, prg_args)

        for level, b in benchmarks.items():
            bench_file = outdir / '{}_level{}.txt'.format(tag, level)
            with open(bench_file, 'w') as outfile:
                outfile.write('\n'.join(b))

    # generate image scripts
    img_benchmarks = []
    for kernel in image_kernels:
        for img in data_img:
            bench = '{}_{}.sh'.format(kernel, img.split(sep='.')[0])
            path = outdir / bench
            img_benchmarks.append(bench)

            prg = './build/{}'.format(kernel)
            prg_args = ['./data/{}'.format(img)]

            print_script(path, prg, prg_args)
    img_benchmarks.sort()
    img_file = outdir / 'img.txt'
    with open(img_file, 'w') as outfile:
        outfile.write('\n'.join(img_benchmarks))


if __name__ == "__main__":
    main()
