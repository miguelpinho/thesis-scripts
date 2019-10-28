#!/bin/bash               
                          
BENCH_DIR="/root/benchmarks"            
KERNEL_DIR="$BENCH_DIR/thesis-kernels"
cd $KERNEL_DIR            
pwd                       
ls                        
                          
./build/dot 2097152 ./data/normal_mu0_0_s45_0_n17000000_seed120197.csv 10000                     
m5 exit                     