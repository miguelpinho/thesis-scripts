#!/usr/bin/env bash

sudo chroot ./mnt /usr/bin/env -i \
    HOME=/root \
    LD_LIBRARY_PATH=/usr/local/lib \
    /bin/bash