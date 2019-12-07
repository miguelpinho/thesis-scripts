#!/bin/bash               
                          
BENCH_DIR="/root/benchmarks"            
KERNEL_DIR="$BENCH_DIR/thesis-kernels"
cd $KERNEL_DIR            
pwd                       
ls                        
                          
./build/iamax 65536 ./data/lognormal_mu5_0_s3_5_n17000000_seed270955.csv 400                     
m5 exit                     