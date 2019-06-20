#!/bin/bash

BENCH_DIR="/root/benchmarks"
APP_DIR="$BENCH_DIR/thesis-apps/integerNeuralNetwork"
cd $APP_DIR
pwd
ls

./intNN
m5 exit
