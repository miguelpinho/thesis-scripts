#!/bin/bash

BENCH_DIR="/root/benchmarks"
APP_DIR="$BENCH_DIR/thesis-apps/minimap2"
cd $APP_DIR
pwd
ls

./minimap2 -a test/MT-human.fa test/MT-orang.fa > /dev/null
m5 exit
