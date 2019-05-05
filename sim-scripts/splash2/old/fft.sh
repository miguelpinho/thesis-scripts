#!/bin/bash

m5 dumpresetstats
./home/splash2/codes/kernels/fft/FFT
m5 dumpresetstats
m5 exit
