#!/bin/bash

export M5_PATH=/homelocal/mpinho-local/fs-files
export GEM5_PATH=/homelocal/mpinho-local/gem5-thesis

export DATE=24-april-2019

parallel ../util/run_fs_1cpu.sh ::: ../spec2006/libquantum.sh ../spec2006/hmmer.sh
