#!/bin/bash

SPEC_DIR="/home/spec_cpu2006-1.2"
cd $SPEC_DIR
pwd
ls

m5 resetstats
./benchspec/CPU2006/456.hmmer/exe/hmmer_base.gcc83-aarch64 \
    ./benchspec/CPU2006/456.hmmer/data/test/input/bombesin.hmm
m5 dumpresetstats
m5 exit
