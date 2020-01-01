#!/usr/bin/env bash

source .env

echo "Running gem5 build in $GEM5_PATH"

echo "Backup $GEM5_PATH/configs/common/cores/arm/O3_ARM_v7a.py"
mv $GEM5_PATH/configs/common/cores/arm/O3_ARM_v7a.py \
	$GEM5_PATH/configs/common/cores/arm/O3_ARM_v7a.py.backup

declare -A config
config[LP_NF]  = "lowp_nofuse.py"
config[LP_F]   = "lowp_fuse.py"
config[LP_FP]  = "lowp_fusepenalty.py"
config[HP3_NF] = "highp_nofuse_3fu.py"
config[HP2_NF] = "highp_nofuse_2fu.py"
config[HP1_NF] = "highp_nofuse_1fu.py"
config[HP3_F]  = "highp_fuse_3fu.py"
config[HP2_F]  = "highp_fuse_2fu.py"
config[HP1_F]  = "highp_fuse_1fu.py"
config[HP3_FP] = "highp_fusepenalty_3fu.py"
config[HP2_FP] = "highp_fusepenalty_2fu.py"
config[HP1_FP] = "highp_fusepenalty_1fu.py"

for cfg in "${!config[@]}"; do
	printf "\nRun %s config:\n" $cfg
	cp ./o3-configs/${config[$cfg]} $GEM5_PATH/configs/common/cores/arm/O3_ARM_v7a.py
	./rungem5-fs.py --runs=1 --run-tag=$cfg scriptset ./sim-scripts/thesis-benchmarks.txt
done

printf "\nRestore %s/configs/common/cores/arm/O3_ARM_v7a.py" $GEM5_PATH
mv $GEM5_PATH/configs/common/cores/arm/O3_ARM_v7a.py.backup \
	$GEM5_PATH/configs/common/cores/arm/O3_ARM_v7a.py
