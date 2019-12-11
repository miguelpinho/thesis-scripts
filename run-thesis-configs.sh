#!/usr/bin/env bash

source .env

echo "Running gem5 build in $GEM5_PATH"

echo "Backup $GEM5_PATH/configs/common/cores/arm/O3_ARM_v7a.py"
mv $GEM5_PATH/configs/common/cores/arm/O3_ARM_v7a.py \
	$GEM5_PATH/configs/common/cores/arm/O3_ARM_v7a.py.backup

declare -A config
config[NF_4]="O3_ARM_v7a_nofuse_4fu.py"
config[F_4]="O3_ARM_v7a_fuse_4fu.py"
config[NF_2]="O3_ARM_v7a_nofuse_2fu.py"
config[F_2]="O3_ARM_v7a_fuse_2fu.py"
config[NF_1]="O3_ARM_v7a_nofuse_1fu.py"
config[F_1]="O3_ARM_v7a_fuse_1fu.py"
config[A57_NF]="cortex_A57_nofuse.py"
config[A57_F]="cortex_A57_fuse.py"
config[A57_FP]="cortex_A57_fuse_penalty.py"

for cfg in "${!config[@]}"; do
	printf "\nRun %s config:\n" $cfg
	cp ./o3-configs/${config[$cfg]} $GEM5_PATH/configs/common/cores/arm/O3_ARM_v7a.py
	./rungem5-fs.py --runs=1 --run-tag=$cfg scriptset ./sim-scripts/kernels_fast.txt
done

printf "\nRestore %s/configs/common/cores/arm/O3_ARM_v7a.py" $GEM5_PATH
mv $GEM5_PATH/configs/common/cores/arm/O3_ARM_v7a.py.backup \
	$GEM5_PATH/configs/common/cores/arm/O3_ARM_v7a.py
