#!/bin/bash

m5 dumpresetstats
LD_LIBRARY_PATH=./home/ComputeLibrary/build \
    ./home/ComputeLibrary/build/examples/neon_sgemm \
    7 3 5 alpha=1.0f beta=0.0f
m5 dumpresetstats
m5 exit
