#!/usr/bin/env bash

MOUNT="./mnt"

sudo umount $MOUNT/dev
sudo umount $MOUNT/sys
sudo umount $MOUNT/proc

sudo umount $MOUNT
