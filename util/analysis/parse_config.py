#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse
import json
import csv
from pathlib import Path

"""
Util for parsing json config files from gem5.
"""


param = ['widthBlockSize',
         'widthDefinition',
         'widthPackingPolicy',
         'LQEntries',
         'SQEntries',
         'fetchWidth',
         'issueWidth',
         'numIQEntries',
         'numROBEntries',
         'numPhysIntRegs',
         'numPhysFloatRegs',
         'numPhysVecRegs']


def get_args():
    """Return parsed args for op_classes util."""
    parser = argparse.ArgumentParser(
        description='''Parse gem5 json config file'''
    )

    parser.add_argument(
        'in_file',
        help='''Input .json file'''
    )
    parser.add_argument(
        '--out-file',
        default=None,
        help='''Output .csv file'''
    )

    return parser.parse_args()


def parse_config(config):
    info = {}

    # Useful subtrees of the json config.
    cpu = config['system']['switch_cpus'][0]
    fuPool = cpu['fuPool']

    # Get wanted parameters.
    # Bootscript:
    info['bootscript'] = config['system']['readfile']

    # CPU:
    for p in param:
        info[p] = cpu[p]

    # FUPool:
    info['simdCount'] = fuPool['FUList'][5]['count']
    info['simdFuseCap'] = fuPool['FUList'][5]['fuseCap']
    info['fpCount'] = fuPool['FUList'][4]['count']
    info['fpFuseCap'] = fuPool['FUList'][4]['fuseCap']
    info['intAluCount'] = fuPool['FUList'][0]['count']
    info['intComplexCount'] = fuPool['FUList'][1]['count']
    info['loadCount'] = fuPool['FUList'][2]['count']
    info['storeCount'] = fuPool['FUList'][3]['count']

    return info


def main():
    args = get_args()

    in_file = Path(args.in_file)
    if not in_file.is_file():
        print('Invalid input file in_file: {}.'.format(args.in_file))
        sys.exit()

    with open(in_file) as f:
        config = json.load(f)
    
    info = parse_config(config)

    if args.out_file is None:
        w = csv.writer(sys.stdout)
        w.writerow(info.keys())
        w.writerow(info.values())
    else:
        out_file = Path(args.out_file)

        # https://stackoverflow.com/questions/10373247/how-do-i-write-a-python-dictionary-to-a-csv-file
        with open(out_file, 'w') as f:
            w = csv.writer(f)
            w.writerow(info.keys())
            w.writerow(info.values())


if __name__ == "__main__":
    main()
