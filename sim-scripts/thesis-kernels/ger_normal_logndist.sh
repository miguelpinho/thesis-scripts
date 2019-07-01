#!/bin/bash               
                          
BENCH_DIR="/root/benchmarks"            
KERNEL_DIR="$BENCH_DIR/thesis-kernels"
cd $KERNEL_DIR            
pwd                       
ls                        
                          
./build/ger 512 512 ./data/lognormal_mu5_0_s3_5_n4194304_seed968017.csv                     
m5 exit                     