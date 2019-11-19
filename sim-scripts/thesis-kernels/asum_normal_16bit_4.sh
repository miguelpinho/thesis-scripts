#!/bin/bash               
                          
BENCH_DIR="/root/benchmarks"            
KERNEL_DIR="$BENCH_DIR/thesis-kernels"
cd $KERNEL_DIR            
pwd                       
ls                        
                          
./build/asum 65536 ./data/lognormal_mu5_0_s3_5_n17000000_seed568863.csv 400                     
m5 exit                     