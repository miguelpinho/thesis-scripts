#!/bin/bash               
                          
BENCH_DIR="/root/benchmarks"            
KERNEL_DIR="$BENCH_DIR/thesis-kernels"
cd $KERNEL_DIR            
pwd                       
ls                        
                          
./build/iamax 65536 ./data/normal_mu0_0_s65_0_n17000000_seed485805.csv 400                     
m5 exit                     