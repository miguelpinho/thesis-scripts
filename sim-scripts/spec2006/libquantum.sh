#!/bin/bash

SPEC_DIR="/home/spec_cpu2006-1.2"
cd $SPEC_DIR
pwd
ls

m5 dumpresetstats
./benchspec/CPU2006/462.libquantum/exe/libquantum_base.arm-64bit 1397 8
m5 dumpresetstats
m5 exit