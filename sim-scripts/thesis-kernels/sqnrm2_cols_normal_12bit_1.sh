#!/bin/bash               
                          
BENCH_DIR="/root/benchmarks"            
KERNEL_DIR="$BENCH_DIR/thesis-kernels"
cd $KERNEL_DIR            
pwd                       
ls                        
                          
./build/sqnrm2_cols 1024 2048 ./data/lognormal_mu4_0_s2_2_n17000000_seed161353.csv 200                     
m5 exit                     