#!/bin/bash

BENCH_DIR="/root/benchmarks"
KERNEL_DIR="$BENCH_DIR/thesis-kernels"
cd $KERNEL_DIR
pwd
ls

./build/gemm 100 100 100 ./data/lognormal_mu6_0_s3_2_n30000_seed321600.csv
m5 exit
