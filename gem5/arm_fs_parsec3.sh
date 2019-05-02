#!/bin/bash

DATE=$(LANG=en_us_88591; date "+%d-%b-%Y")

OUT_DIR=$M5OUT_PATH/${DATE,,}/fs-parsec3

find ../sim-scripts/parsec-3.0/ -name "*sh" | parallel -I% --max-args 1 ../util/run_fs_1cpu.sh % %
