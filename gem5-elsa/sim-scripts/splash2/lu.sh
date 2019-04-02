#!/bin/bash

m5 dumpresetstats
./home/splash2/codes/kernels/lu/non_contiguous_blocks/LU
m5 dumpresetstats
m5 exit
