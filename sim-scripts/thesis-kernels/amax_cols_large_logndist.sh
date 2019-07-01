#!/bin/bash               
                          
BENCH_DIR="/root/benchmarks"            
KERNEL_DIR="$BENCH_DIR/thesis-kernels"
cd $KERNEL_DIR            
pwd                       
ls                        
                          
./build/amax_cols 1024 1024 ./data/lognormal_mu5_0_s3_5_n4194304_seed508617.csv                     
m5 exit                     