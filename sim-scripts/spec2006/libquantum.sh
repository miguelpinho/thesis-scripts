#!/bin/bash

SPEC_DIR="/home/spec_cpu2006-1.2"
cd $SPEC_DIR
pwd
ls

m5 resetstats
./benchspec/CPU2006/462.libquantum/exe/libquantum_base.gcc83-aarch64 \
    1397 8
m5 dumpstats
m5 exit
