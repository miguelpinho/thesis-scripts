#!/bin/bash

DATE=$(LANG=en_us_88591; date "+%d-%b-%Y")

OUT_DIR=$M5OUT_PATH/${DATE,,}/fs-spec2006

parallel ../util/run_fs_1cpu.sh ::: ../spec2006/libquantum.sh ../spec2006/hmmer.sh ::: libquantum hmmer
