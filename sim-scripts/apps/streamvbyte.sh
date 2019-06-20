#!/bin/bash

BENCH_DIR="/root/benchmarks"
APP_DIR="$BENCH_DIR/thesis-apps/streamvbyte"
cd $APP_DIR
pwd
ls

./example
m5 exit
