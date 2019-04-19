#!/bin/bash

export M5_PATH=/homelocal/mpinho-local/fs-files
GEM5_PATH=/homelocal/mpinho-local/gem5-thesis

DATE=19-april-2019

OUT_DIR=/homelocal/mpinho-local/output/$DATE/fs

$GEM5_PATH/build/ARM/gem5.opt \
    -d $OUT_DIR -re \
    $GEM5_PATH/configs/example/fs.py \
    --machine-type=VExpress_GEM5_V1 \
    --kernel=$M5_PATH/binaries/vmlinux.vexpress_gem5_v1_64 \
    --disk-image=$M5_PATH/disks/benchmarks.img \
    --dtb-filename=$M5_PATH/binaries/armv8_gem5_v1_1cpu.dtb \
    --caches --l2cache
