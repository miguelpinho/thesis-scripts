#!/bin/bash               
                          
BENCH_DIR="/root/benchmarks"            
KERNEL_DIR="$BENCH_DIR/thesis-kernels"
cd $KERNEL_DIR            
pwd                       
ls                        
                          
./build/iamax 4194304 ./data/lognormal_mu5_0_s3_5_n17000000_seed357477.csv 10000                     
m5 exit                     