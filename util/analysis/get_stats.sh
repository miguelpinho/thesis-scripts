#!/usr/bin/env bash

DIR="${BASH_SOURCE%/*}"
if [[ ! -d "$DIR" ]]; then DIR="$PWD"; fi

find $1 -name 'stats.txt' | parallel --bar "awk -f $DIR/clean_stats.awk {} > {//}/roi.txt"
find $1 -name 'roi.txt' | parallel --bar "awk -f $DIR/time.awk {} > {//}/time.csv"
find $1 -name 'roi.txt' | parallel --bar "awk -f $DIR/stat.awk -v stat='{2}' {1} | csvtool transpose - > {1//}/{2}.csv" :::: - ::: simd_fu_used simd_fu_extra simd_fu_issued simd_fu_width fp_simd_fu_used
find $1 -name 'roi.txt' | parallel --bar "awk -f $DIR/stat.awk -v stat='widthClass' {1} | csvtool transpose - > {1//}/width_class.csv"
find $1 -name 'roi.txt' | parallel --bar "awk -f $DIR/stat.awk -v stat='FU_type_0' {1} | csvtool transpose - > {1//}/iq_fu_class.csv"
find $1 -name 'roi.txt' | parallel --bar "awk -f $DIR/stat_vector.awk -v stat='{2}' {1} | $DIR/csvpivot.py 'fu' > {1//}/{2}.csv" :::: - ::: simd_fu_issue_partial simd_fu_width_partial
find $1 -name 'roi.txt' | parallel --bar "awk -f $DIR/stat_by_class.awk -v stat='{2}' {1} | $DIR/csvpivot.py 'class' > {1//}/{2}.csv" :::: - ::: statVectorInstTotalWidthByClass
find $1 -name 'roi.txt' | parallel --bar "awk -f $DIR/width.awk {} > {//}/width.csv"
find $1 -name 'roi.txt' | parallel --bar "$DIR/../mcpat/GEM5ToMcPAT.py --quiet --out={//}/mcpat.xml {} {//}/config.json {//}/../../template.xml"
find $1 -name 'roi.txt' | parallel --bar "$DIR/../mcpat/GEM5ToMcPAT.py --quiet --out={//}/mcpat_clkgated.xml {} {//}/config.json {//}/../../template-clkgated.xml"
if [[ $MCPAT ]]; then
    find $1 -name 'mcpat.xml' | parallel --bar "$MCPAT -infile {} -print_level 5 -opt_for_clk 0 > {//}/power.txt"
    find $1 -name 'mcpat_clkgated.xml' | parallel --bar "$MCPAT -infile {} -print_level 5 -opt_for_clk 0 > {//}/power_clkgated.txt"
else
    echo "No path for MCPAT provided."
fi
find $1 -name 'power.txt' | parallel --bar "$DIR/../mcpat/mcpat_tocsv.py {} > {.}.csv"
find $1 -name 'power_clkgated.txt' | parallel --bar "$DIR/../mcpat/mcpat_tocsv.py {} > {.}.csv"
