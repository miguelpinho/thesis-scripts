#!/bin/bash               
                          
BENCH_DIR="/root/benchmarks"            
KERNEL_DIR="$BENCH_DIR/thesis-kernels"
cd $KERNEL_DIR            
pwd                       
ls                        
                          
./build/gemm 1048 524 524 ./data/lognormal_mu5_0_s3_5_n17000000_seed568863.csv 5                     
m5 exit                     