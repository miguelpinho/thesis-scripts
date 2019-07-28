#!/bin/bash               
                          
BENCH_DIR="/root/benchmarks"            
KERNEL_DIR="$BENCH_DIR/thesis-kernels"
cd $KERNEL_DIR            
pwd                       
ls                        
                          
./build/sqnrm2_cols 16384 8192 ./data/lognormal_mu5_0_s3_5_n4194304_seed742922.csv                     
m5 exit                     