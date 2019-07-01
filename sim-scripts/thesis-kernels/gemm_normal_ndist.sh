#!/bin/bash               
                          
BENCH_DIR="/root/benchmarks"            
KERNEL_DIR="$BENCH_DIR/thesis-kernels"
cd $KERNEL_DIR            
pwd                       
ls                        
                          
./build/gemm 512 512 512 ./data/normal_mu0_0_s10000_0_n4194304_seed9705.csv                     
m5 exit                     