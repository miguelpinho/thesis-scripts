#!/bin/bash               
                          
BENCH_DIR="/root/benchmarks"            
KERNEL_DIR="$BENCH_DIR/thesis-kernels"
cd $KERNEL_DIR            
pwd                       
ls                        
                          
./build/amax_cols 1024 2048 ./data/normal_mu0_0_s65_0_n17000000_seed358739.csv 200                     
m5 exit                     