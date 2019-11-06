#!/bin/bash               
                          
BENCH_DIR="/root/benchmarks"            
KERNEL_DIR="$BENCH_DIR/thesis-kernels"
cd $KERNEL_DIR            
pwd                       
ls                        
                          
./build/img_erode ./third_party/ComputeLibrary/data/images/800x600.ppm
m5 exit                     