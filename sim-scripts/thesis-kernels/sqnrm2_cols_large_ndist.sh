#!/bin/bash               
                          
BENCH_DIR="/root/benchmarks"            
KERNEL_DIR="$BENCH_DIR/thesis-kernels"
cd $KERNEL_DIR            
pwd                       
ls                        
                          
./build/sqnrm2_cols 1024 1024 ./data/normal_mu0_0_s10000_0_n4194304_seed9705.csv                     
m5 exit                     