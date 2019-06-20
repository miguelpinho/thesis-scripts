#!/bin/bash

BENCH_DIR="/root/benchmarks"
PARSEC_DIR="$BENCH_DIR/parsec-3.0"
cd $PARSEC_DIR
pwd

source ./env.sh
parsecmgmt -a run -p splash2.ocean_cp -c gcc-hooks -i simsmall -n 1
m5 exit
