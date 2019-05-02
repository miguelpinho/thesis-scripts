#!/bin/bash

DATE=$(LANG=en_us_88591; date "+%d-%b-%Y")

OUT_DIR=$M5OUT_PATH/${DATE,,}/fs-sve

$GEM5_PATH/build/ARM/gem5.opt \
    -d $OUT_DIR -re \
    $GEM5_SVE_PATH/configs/example/fs.py \
    --arm-sve-vl=4 \
    --machine-type=VExpress_GEM5_V1 \
    --kernel=$M5_PATH/binaries/vmlinux.vexpress_gem5_v1_64 \
    --disk-image=$M5_PATH/disks/benchmarks.img \
    --dtb-filename=$M5_PATH/binaries/armv8_gem5_v1_1cpu.dtb \
    --caches --l2cache
