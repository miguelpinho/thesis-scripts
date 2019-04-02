#!/bin/bash

m5 dumpresetstats
./home/splash2/codes/apps/fmm/FMM < ./home/splash2/codes/apps/fmm/input.256
m5 dumpresetstats
m5 exit
