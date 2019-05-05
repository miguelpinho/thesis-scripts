#!/bin/bash

SCRIPT_PATH=../sim-scripts/spec2006
BENCHMARK_LIST=$SCRIPT_PATH/all.txt

parallel --bar --max-procs $MACHINE_MAX_JOBS \
    ../util/run_fs_1cpu.sh $SCRIPT_PATH/{} {.} :::: $BENCHMARK_LIST
