#!/bin/bash

SPEC_DIR="/home/spec_cpu2006-1.2"
cd $SPEC_DIR
pwd
ls

m5 resetstats
./benchspec/CPU2006/462.libquantum/exe/libquantum_base.gcc83-aarch64 \
    33 5
m5 dumpresetstats
m5 exit
