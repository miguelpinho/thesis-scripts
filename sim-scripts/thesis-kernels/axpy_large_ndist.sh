#!/bin/bash               
                          
BENCH_DIR="/root/benchmarks"            
KERNEL_DIR="$BENCH_DIR/thesis-kernels"
cd $KERNEL_DIR            
pwd                       
ls                        
                          
./build/axpy 1073741824 ./data/normal_mu0_0_s10000_0_n4194304_seed11904.csv                     
m5 exit                     