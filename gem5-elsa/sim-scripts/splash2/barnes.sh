#!/bin/bash

m5 dumpresetstats
./home/splash2/codes/apps/fmm/BARNES < ./home/splash2/codes/apps/fmm/input
m5 dumpresetstats
m5 exit
