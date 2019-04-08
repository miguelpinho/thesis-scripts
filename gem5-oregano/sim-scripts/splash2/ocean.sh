#!/bin/bash

m5 dumpresetstats
./home/splash2/codes/apps/ocean/non_contiguous_partitions/OCEAN
m5 dumpresetstats
m5 exit
