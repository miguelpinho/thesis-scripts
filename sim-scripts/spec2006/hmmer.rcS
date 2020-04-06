#!/bin/bash

BENCH_DIR="/root/benchmarks"
SPEC_DIR="$BENCH_DIR/spec_cpu2006-1.2"
cd $SPEC_DIR
pwd
ls

m5 dumpresetstats
./benchspec/CPU2006/456.hmmer/exe/hmmer_base.gcc83-aarch64 \
    ./benchspec/CPU2006/456.hmmer/data/train/input/leng100.hmm
m5 dumpresetstats
m5 exit
