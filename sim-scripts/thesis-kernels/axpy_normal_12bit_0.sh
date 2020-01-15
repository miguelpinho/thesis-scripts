#!/bin/bash               
                          
BENCH_DIR="/root/benchmarks"            
KERNEL_DIR="$BENCH_DIR/thesis-kernels"
cd $KERNEL_DIR            
pwd                       
ls                        
                          
./build/axpy 65536 ./data/lognormal_mu4_0_s2_2_n17000000_seed125529.csv 400                     
m5 exit                     