#!/bin/bash

SCRIPT_PATH=../sim-scripts/spec2006
BENCHMARK_LIST=$SCRIPT_PATH/small.txt
OUT_DIR=fs-spec2006-width_3

parallel --bar --max-procs $MACHINE_MAX_JOBS \
    ../util/run_fs_1cpu_width.sh $SCRIPT_PATH/{} $OUT_DIR/{.} :::: $BENCHMARK_LIST
