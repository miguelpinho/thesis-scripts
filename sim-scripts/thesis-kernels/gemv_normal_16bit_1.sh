#!/bin/bash               
                          
BENCH_DIR="/root/benchmarks"            
KERNEL_DIR="$BENCH_DIR/thesis-kernels"
cd $KERNEL_DIR            
pwd                       
ls                        
                          
./build/gemv 1024 2048 ./data/lognormal_mu5_0_s3_3_n17000000_seed289906.csv 200                     
m5 exit                     