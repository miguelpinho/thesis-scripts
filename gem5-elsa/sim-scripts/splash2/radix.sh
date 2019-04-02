#!/bin/bash

m5 resetstats
./home/splash2/codes/kernels/fft/RADIX
m5 dumpstats
m5 exit
