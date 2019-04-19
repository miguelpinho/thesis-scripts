export M5_PATH=/home/miguelp/gem5-full-system/aarch-system-20180409
GEM5_PATH=/home/miguelp/gem5

$GEM5_PATH/build/ARM/gem5.opt \
    -d /home/miguelp/Documents/Blue/prototype/fs-logs/trusty -re \
    $GEM5_PATH/configs/example/fs.py \
    --machine-type=VExpress_GEM5_V1 \
    --kernel=$M5_PATH/binaries/vmlinux.vexpress_gem5_v1_64 \
    --disk-image=$M5_PATH/disks/parsec3.img \
    --dtb-filename=$M5_PATH/binaries/armv8_gem5_v1_1cpu.dtb \
    --caches --l2cache \
    --script ../sim-scripts/checkpoint.sh
