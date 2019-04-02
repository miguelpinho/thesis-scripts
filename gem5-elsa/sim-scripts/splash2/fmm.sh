#!/bin/bash

m5 resetstats
./home/splash2/codes/apps/fmm/FMM
m5 dumpstats
m5 exit
