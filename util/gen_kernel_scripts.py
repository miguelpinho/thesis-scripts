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
    'tiny': {
        1:{'iter':'1500', 'shape':['8192']},
        2:{'iter':'150', 'shape':['1024 1024', '512 2048', '2048 512', '256 4096', '4096 256']},
        3:{'iter':'5'  , 'shape':['524 524 524', '524 1048 256', '524 256 1048', '1048 256 524', '1048 524 256']}
    },
    'small': {
        1:{'iter':'400', 'shape':['65536']},
        2:{'iter':'200', 'shape':['2048 1024', '1024 2048', '4096 512', '512 4096', '256 8192']},
        3:{'iter':'5'  , 'shape':['1048 524 524', '524 1048 524', '524 524 1048', '1048 256 1048', '1048 1048 256']}
    }
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
image_kernels = {
    'tiny': {
        'conv':6,
        'img_hist':9,
        'img_integral':18,
        'img_erode':45,
        'img_canny':3,
        'img_cartoon':6,
        'img_yuv444':90,
        'img_median':30,
        'img_scale':3
    },
    'small': {
        'conv':10,
        'img_hist':15,
        'img_integral':30,
        'img_erode':75,
        'img_canny':5,
        'img_cartoon':10,
        'img_yuv444':150,
        'img_median':50,
        'img_scale':5
    }
}

# ppm image files
data_img = {
    'tiny': [
        'image1_50per.ppm',
        'image2_50per.ppm',
        'image3_50per.ppm',
        'image4_50per.ppm',
        'image5_50per.ppm'
    ],
    'small': [
        'image1.ppm',
        'image2.ppm',
        'image3.ppm',
        'image4.ppm',
        'image5.ppm'
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

    # generate algebra scripts
    for tag, arguments in workload_sizes.items():
        benchmarks = {1:[], 2:[], 3:[]}

        for kernel in algebra_kernels:
            for d, data in data_dist.items():
                blas = kernel[0]
                level = kernel[1]

                for idx, data_file in enumerate(data):
                    bench = '{}_{}_{}_{}.rcS'.format(blas, tag, d, idx)
                    path = outdir / bench
                    benchmarks[level].append(bench)

                    prg = './build/{}'.format(blas)
                    prg_args = []
                    prg_args.append(arguments[level]['shape'][idx % len(arguments[level]['shape'])])
                    prg_args.append("./data/{}".format(data_file))
                    prg_args.append(arguments[level]['iter'])

                    print_script(path, prg, prg_args)

        for level, b in benchmarks.items():
            bench_file = outdir / 'blas_level{1}_{0}.txt'.format(tag, level)
            with open(bench_file, 'w') as outfile:
                outfile.write('\n'.join(b))

    # generate image scripts
    for tag, img_kernels in image_kernels.items():
        img_benchmarks = []
        for kernel, iterations in img_kernels.items():
            for img in data_img[tag]:
                bench = '{}_{}_{}.rcS'.format(kernel, tag, img.split(sep='.')[0])
                path = outdir / bench
                img_benchmarks.append(bench)

                prg = './build/{}'.format(kernel)
                prg_args = ['./data/{}'.format(img), str(iterations)]

                print_script(path, prg, prg_args)
        img_benchmarks.sort()
        img_file = outdir / 'img_{}.txt'.format(tag)
        with open(img_file, 'w') as outfile:
            outfile.write('\n'.join(img_benchmarks))


if __name__ == "__main__":
    main()
