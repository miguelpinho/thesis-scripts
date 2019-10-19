#!/bin/bash

SCRIPT_PATH=../sim-scripts/spec2006
BENCHMARK_LIST=$SCRIPT_PATH/small.txt
OUT_DIR=fs-spec2006

parallel --bar --max-procs $MACHINE_MAX_JOBS \
    ../util/run_fs_1cpu.sh $SCRIPT_PATH/{} $OUT_DIR/{.} :::: $BENCHMARK_LIST