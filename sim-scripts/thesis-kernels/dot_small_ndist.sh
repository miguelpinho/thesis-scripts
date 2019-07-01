#!/bin/bash               
                          
BENCH_DIR="/root/benchmarks"            
KERNEL_DIR="$BENCH_DIR/thesis-kernels"
cd $KERNEL_DIR            
pwd                       
ls                        
                          
./build/dot 256 ./data/normal_mu0_0_s10000_0_n4194304_seed458196.csv                     
m5 exit                     