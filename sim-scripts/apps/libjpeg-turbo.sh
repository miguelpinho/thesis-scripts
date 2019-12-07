#!/bin/bash

BENCH_DIR="/root/benchmarks"
APP_DIR="$BENCH_DIR/thesis-apps/lib_jpegturbo"
cd $APP_DIR
pwd
ls

./build/tjbench ./testimages/vgl_6434_0018a.bmp 95 -rgb -qq -nowrite -warmup 10
m5 exit
