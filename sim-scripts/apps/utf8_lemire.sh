#!/bin/bash

BENCH_DIR="/root/benchmarks"
APP_DIR="$BENCH_DIR/thesis-apps/utf8"
cd $APP_DIR
pwd
ls

./utf8 bench lemire
m5 exit
