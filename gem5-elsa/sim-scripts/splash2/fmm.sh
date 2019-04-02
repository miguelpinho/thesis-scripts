#!/bin/bash

m5 resetstats
./home/splash2/codes/apps/fmm/FMM < ./home/splash2/codes/apps/fmm/input.256
m5 dumpstats
m5 exit
