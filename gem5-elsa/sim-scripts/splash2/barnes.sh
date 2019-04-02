#!/bin/bash

m5 resetstats
./home/splash2/codes/apps/fmm/BARNES < ./home/splash2/codes/apps/fmm/input
m5 dumpstats
m5 exit
