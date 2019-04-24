#!/bin/bash

export M5_PATH=/home/miguelp/gem5-full-system/aarch-system-20180409
export GEM5_PATH=/home/miguelp/gem5-test

export DATE=24-april-2019

parallel ../util/run_fs_1cpu.sh ::: ../spec2006/libquantum.sh ../spec2006/hmmer.sh ::: libquantum hmmer
