#!/usr/bin/env bash

DISK="ubuntu-14.04.img"
MOUNT="./mnt"
OFFSET=1048576

sudo mount -o loop,rw,offset=$OFFSET $DISK $MOUNT

sudo mount -o bind /dev $MOUNT/dev
sudo mount -o bind /sys $MOUNT/sys
sudo mount -o bind /proc $MOUNT/proc
