#!/usr/bin/env bash

sudo mount -o loop,rw,offset=1048576 ubuntu-14.04.img ./mnt/

sudo mount -o bind /dev ./mnt/dev
sudo mount -o bind /sys ./mnt/sys
sudo mount -o bind /proc ./mnt/proc