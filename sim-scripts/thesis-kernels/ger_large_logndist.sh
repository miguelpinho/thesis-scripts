#!/bin/bash               
                          
BENCH_DIR="/root/benchmarks"            
KERNEL_DIR="$BENCH_DIR/thesis-kernels"
cd $KERNEL_DIR            
pwd                       
ls                        
                          
./build/ger 1024 1024 ./data/lognormal_mu5_0_s3_5_n4194304_seed594722.csv                     
m5 exit                     