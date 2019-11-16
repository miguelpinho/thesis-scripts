#!/bin/bash               
                          
BENCH_DIR="/root/benchmarks"            
KERNEL_DIR="$BENCH_DIR/thesis-kernels"
cd $KERNEL_DIR            
pwd                       
ls                        
                          
./build/fft 262144 ./data/lognormal_mu5_0_s3_5_n17000000_seed1750.csv 200                     
m5 exit                     