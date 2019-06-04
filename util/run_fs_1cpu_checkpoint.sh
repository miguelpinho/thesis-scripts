#!/bin/bash

DATE=$(LANG=en_us_88591; date "+%d-%b-%Y")

OUT_DIR=$M5OUT_PATH/${DATE,,}/$2

# Run gem5 FS.
$GEM5_PATH/build/ARM/gem5.opt \
    -d $OUT_DIR -re \
    $GEM5_PATH/configs/example/fs.py \
    --machine-type=VExpress_GEM5_V1 \
    --kernel=$M5_PATH/binaries/vmlinux.vexpress_gem5_v1_64 \
    --disk-image=$M5_PATH/disks/benchmarks.img \
    --dtb-filename=$M5_PATH/binaries/armv8_gem5_v1_1cpu.dtb \
    --cpu-type=AtomicSimpleCPU \
    --caches --l2cache \
    --checkpoint-dir=$GEM5_CKPOINT_PATH/fs \
    --checkpoint-restore 1 \
    --take-checkpoints=1500000000000,10000000000 \
    --restore-with-cpu=AtomicSimpleCPU \
    --script=$1

