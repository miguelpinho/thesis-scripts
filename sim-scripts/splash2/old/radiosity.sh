#!/bin/bash

m5 dumpresetstats
./home/splash2/codes/apps/radiosity/RADIOSITY
m5 dumpresetstats
m5 exit
