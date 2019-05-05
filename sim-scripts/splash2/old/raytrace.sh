#!/bin/bash

m5 dumpresetstats
./home/splash2/codes/apps/raytrace/RAYTRACE \
    ./home/splash2/codes/apps/raytrace/input/balls4.env.Z
m5 dumpresetstats
m5 exit
