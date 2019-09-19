#!/usr/bin/env bash

find . -name 'stats.txt' | parallel 'awk -f clean_stats.awk {} > {//}/roi_stats.txt'
find . -name 'stats.txt' | parallel 'awk -f time.awk {} | csvtool transpose - > {//}/time.csv'
find . -name 'roi_stats.txt' > stat_files.txt
parallel 'awk -f stat.awk -v stat="{2}" {1} | csvtool transpose - | csvcut -C samples,mean,stdev,underflows,overflows,min_value,max_value,total > {1//}/{2}.csv' :::: stat_files.txt :::: stat_list.txt
parallel 'awk -f stat_vector.awk -v stat="{2}" {1} | ./csvpivot.py "fu" | csvcut -C samples,mean,stdev,underflows,overflows,min_value,max_value,total > {1//}/{2}.csv' :::: stat_files.txt :::: stat_vector_list.txt
parallel 'awk -f stat_by_class.awk -v stat="{2}" {1} | ./csvpivot.py "class" | csvcut -C samples,mean,stdev,underflows,overflows,min,max,total > {1//}/{2}.csv' :::: stat_files.txt :::: stat_by_class_list.txt
parallel 'awk -f stat.awk -v stat="widthClass" {1} | csvtool transpose - | csvcut -C total > {1//}/width_class.csv' :::: stat_files.txt
parallel './stats_concat.py {1} {2}.csv' :::: folders.txt ::: 'time'
parallel './stats_concat.py {1} {2}.csv' :::: folders.txt :::: stat_list.txt stat_vector_list.txt
parallel './stats_concat.py {1} {2}.csv' :::: folders.txt ::: 'width_class'

