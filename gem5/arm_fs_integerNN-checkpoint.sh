#!/bin/bash

SCRIPT_PATH=../sim-scripts/apps
BENCHMARK_LIST=$SCRIPT_PATH/all.txt
OUT_DIR=apps-ckpoints

parallel --bar --max-procs $MACHINE_MAX_JOBS \
    ../util/run_fs_1cpu.sh $SCRIPT_PATH/{} $OUT_DIR/{.} :::: $BENCHMARK_LIST
