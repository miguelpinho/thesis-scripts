#!/bin/bash

export M5_PATH=/homelocal/mpinho-local/fs-files
GEM5_PATH=/homelocal/mpinho-local/gem5-thesis

DATE=3-april-2019

OUT_DIR=/homelocal/mpinho-local/output/$DATE/splash2
SCRIPT_LIST=(radix barnes fft fmm)
# SCRIPT_LIST=(lu raytrace cholesky ocean)
# SCRIPT_LIST=(water-nsquared radiosity)

for script in ${SCRIPT_LIST[@]}; do {
    $GEM5_PATH/build/ARM/gem5.opt \
        -d "$OUT_DIR-$script" -re \
        $GEM5_PATH/configs/example/fs.py \
        --machine-type=VExpress_GEM5_V1 \
        --kernel=$M5_PATH/binaries/vmlinux.vexpress_gem5_v1_64 \
        --disk-image=$M5_PATH/disks/benchmarks.img \
        --dtb-filename=$M5_PATH/binaries/armv8_gem5_v1_1cpu.dtb \
        --caches --l2cache \
        --checkpoint-dir=./checkpoints \
        --checkpoint-restore 1 \
        --restore-with-cpu=O3_ARM_v7a_3 \
        --script="./sim-scripts/splash2/$script.sh" & pid=$!
    PID_LIST+=" $pid";
} done

trap "kill $PID_LIST" SIGINT

echo "SPLASH-2 benchmarks have started.";

wait $PID_LIST

echo
echo "All benchmarks have ended.";
