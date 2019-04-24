#!/bin/bash

export M5_PATH=/home/miguelp/gem5-full-system/aarch-system-20180409
export GEM5_PATH=/home/miguelp/gem5-test

export DATE=24-april-2019

find ../sim-scripts/parsec-3.0/ -name "*sh" | parallel -I% --max-args 1 /bin/bash ../util/run_fs_1cpu.sh % %
