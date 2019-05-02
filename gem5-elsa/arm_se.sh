#!/bin/bash

BENCHMARKS_PATH=/homelocal/mpinho-local/benchmarks
GEM5_PATH=/homelocal/mpinho-local/gem5-thesis

DATE=19-april-2019

OUT_DIR=/homelocal/mpinho-local/output/$DATE/se

$GEM5_PATH/build/ARM/gem5.opt \
    -d $OUT_DIR -re \
    --debug-flags=O3PipeView --debug-file=trace.txt \
    $GEM5_PATH/configs/example/se.py \
    --cpu-type=O3_ARM_v7a_3 --caches --l2cache \
    -c $BENCHMARKS_PATH/custom/tests_eigen
