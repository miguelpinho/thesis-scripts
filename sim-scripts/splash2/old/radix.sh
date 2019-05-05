#!/bin/bash

m5 dumpresetstats
./home/splash2/codes/kernels/radix/RADIX
m5 dumpresetstats
m5 exit
