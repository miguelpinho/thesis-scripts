#!/bin/bash               
                          
BENCH_DIR="/root/benchmarks"            
KERNEL_DIR="$BENCH_DIR/thesis-kernels"
cd $KERNEL_DIR            
pwd                       
ls                        
                          
./build/axpy 262144 ./data/lognormal_mu5_0_s3_5_n17000000_seed270955.csv 200                     
m5 exit                     