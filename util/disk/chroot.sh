#!/usr/bin/env bash

sudo chroot ./mnt /usr/bin/env -i \
    LOGNAME=root \
    USERNAME=root \
    HOME=/root \
    TERM="$TERM" \
    COLORTERM=truecolor \
    PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
    LD_LIBRARY_PATH=/usr/local/lib \
    /bin/bash