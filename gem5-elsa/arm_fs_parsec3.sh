#!/bin/bash

export M5_PATH=/homelocal/mpinho-local/fs-files
export GEM5_PATH=/homelocal/mpinho-local/gem5-thesis

export DATE=19-april-2019

find ../sim-scripts/parsec-3.0/ -name "*sh" | parallel -I% --max-args 1 /bin/bash ../util/run_fs_1cpu.sh % %
