#!/bin/bash               
                          
BENCH_DIR="/root/benchmarks"            
KERNEL_DIR="$BENCH_DIR/thesis-kernels"
cd $KERNEL_DIR            
pwd                       
ls                        
                          
./build/sqnrm2_cols 2048 1024 ./data/normal_mu0_0_s65_0_n17000000_seed803661.csv 200                     
m5 exit                     