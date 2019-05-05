#!/bin/bash

m5 dumpresetstats
./home/splash2/codes/apps/water-nsquared/WATER-NSQUARED \
    < ./home/splash2/codes/apps/water-nsquared/input
m5 dumpresetstats
m5 exit
