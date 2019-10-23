#!/bin/bash               
                          
BENCH_DIR="/root/benchmarks"            
KERNEL_DIR="$BENCH_DIR/thesis-kernels"
cd $KERNEL_DIR            
pwd                       
ls                        
                          
./build/gemv 4096 4096 ./data/lognormal_mu5_0_s3_5_n17000000_seed357477.csv 10                     
m5 exit                     