#!/bin/bash

PARSEC_DIR="/home/parsec-3.0"
cd $PARSEC_DIR
pwd

source ./env.sh
parsecmgmt -a run -p splash2x.fmm -c gcc-hooks -i simsmall -n 1
m5 exit
