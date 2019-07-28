#!/bin/bash               
                          
BENCH_DIR="/root/benchmarks"            
KERNEL_DIR="$BENCH_DIR/thesis-kernels"
cd $KERNEL_DIR            
pwd                       
ls                        
                          
./build/axpy 4194304 ./data/normal_mu0_0_s10000_0_n100000000_seed901738.csv                     
m5 exit                     