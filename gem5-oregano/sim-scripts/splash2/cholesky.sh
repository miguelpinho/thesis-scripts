#!/bin/bash

m5 dumpresetstats
./home/splash2/codes/kernels/cholesky/CHOLESKY
m5 dumpresetstats
m5 exit
