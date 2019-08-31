#!/usr/bin/env bash

find . -name 'stats.txt' | parallel 'awk -f clean_stats.awk {} > {//}/roi_stats.txt'
find . -name 'roi_stats.txt' > stat_files.txt
parallel 'awk -f stat.awk -v stat="{2}" {1} | csvtool transpose - | csvcut -C samples,mean,stdev,underflows,overflows,min_value,max_value,total > {1//}/{2}.csv' :::: stat_files.txt :::: stat_list.txt
parallel 'awk -f stat_vector.awk -v stat="{2}" {1} | ./csvpivot.py | csvcut -C samples,mean,stdev,underflows,overflows,min_value,max_value,total > {1//}/{2}.csv' :::: stat_files.txt :::: stat_vector_list.txt
parallel './stats_concat.py {1} {2}.csv' ::: fuse no-fuse :::: stat_list.txt stat_vector_list.txt

