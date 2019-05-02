#!/bin/bash

OUT_DIR=/homelocal/mpinho-local/output/$DATE/$2

$GEM5_PATH/build/ARM/gem5.opt \
    -d $OUT_DIR -re \
    $GEM5_PATH/configs/example/fs.py \
    --machine-type=VExpress_GEM5_V1 \
    --kernel=$M5_PATH/binaries/vmlinux.vexpress_gem5_v1_64 \
    --disk-image=$M5_PATH/disks/benchmarks.img \
    --dtb-filename=$M5_PATH/binaries/armv8_gem5_v1_1cpu.dtb \
    --caches --l2cache \
    --checkpoint-dir=../checkpoints \
    --checkpoint-restore 1 \
    --restore-with-cpu=O3_ARM_v7a_3 \
    --script=$1
