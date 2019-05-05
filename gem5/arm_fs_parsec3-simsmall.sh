#!/bin/bash

SCRIPT_PATH=../sim-scripts/parsec3
BENCHMARK_LIST=$SCRIPT_PATH/all-simsmall.txt
OUT_DIR=fs-parsec3

parallel --bar --max-procs $MACHINE_MAX_JOBS \
    ../util/run_fs_1cpu.sh $SCRIPT_PATH/{} $OUT_DIR/{.} :::: $BENCHMARK_LIST