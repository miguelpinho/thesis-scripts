#!/usr/bin/env bash

source .env

printf "Running gem5 build in $GEM5_PATH\n"
date
printf "\n"

./rungem5-fs.py --custom-model-file=o3-configs/configs.txt --width-block 8 --runs=1 --nodes-file=../nodefile.txt scriptset ./sim-scripts/benchmarks.txt

printf "\n"
printf "Finished!\n"
date
