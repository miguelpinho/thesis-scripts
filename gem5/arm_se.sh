#!/bin/bash

DATE=$(LANG=en_us_88591; date "+%d-%b-%Y")

OUT_DIR=$M5OUT_PATH/${DATE,,}/se

$GEM5_PATH/build/ARM/gem5.opt \
    -d $OUT_DIR -re \
    --debug-flags=O3PipeView --debug-file=trace.txt \
    $GEM5_PATH/configs/example/se.py \
    --cpu-type=O3_ARM_v7a_3 --caches --l2cache \
    -c $BENCHMARKS_PATH/custom/tests_eigen
