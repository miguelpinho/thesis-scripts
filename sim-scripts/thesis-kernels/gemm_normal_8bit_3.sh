#!/bin/bash               
                          
BENCH_DIR="/root/benchmarks"            
KERNEL_DIR="$BENCH_DIR/thesis-kernels"
cd $KERNEL_DIR            
pwd                       
ls                        
                          
./build/gemm 1048 256 1048 ./data/normal_mu0_0_s65_0_n17000000_seed611651.csv 5                     
m5 exit                     