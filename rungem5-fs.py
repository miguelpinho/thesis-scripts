#!/usr/bin/env python3

import argparse

parser = argparse.ArgumentParser(description='Run gem5 full-system.')
subparsers = parser.add_subparsers(title='action', help='action to perform')

# "boot" action
parser_boot = subparsers.add_parser('boot', help='boot full-system')

# "checkpoint" action
parser_ckpoint = subparsers.add_parser('checkpoint', help='boot, save checkpoints and exit')

# "restore" action
parser_restore = subparsers.add_parser('restart', help='restore from checkpoint')

# "script" action
parser_script = subparsers.add_parser('script', help='restore and run script')

# "benchmark" action
parser_benchmark = subparsers.add_parser('benchmark', help='restore and run available benchmarks')

