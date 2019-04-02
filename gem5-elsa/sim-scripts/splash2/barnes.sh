#!/bin/bash

m5 dumpresetstats
./home/splash2/codes/apps/barnes/BARNES < ./home/splash2/codes/apps/barnes/input
m5 dumpresetstats
m5 exit
