#!/bin/bash

SCRIPT_PATH=../sim-scripts/spec2006

parallel ../util/run_fs_1cpu.sh \
    ::: $SCRIPT_PATH/libquantum-small.sh $SCRIPT_PATH/hmmer-small.sh \
    :::+ libquantum hmmer
