#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Util and module for running gem5 full-system simulations.
"""

import argparse
import datetime
import subprocess
import os

def get_arguments():
    """Parse rungem5 arguments."""
    parser = argparse.ArgumentParser(description='Run gem5 full-system.')
    subparsers = parser.add_subparsers(title='action', help='action to perform')

    # generic options
    # env
    parser.add_argument(
        '--env-file',
        help='''Script file frow where to load environment variables.'''
    )
    parser.add_argument(
        '--gem5-path',
        help='''Path to the gem5 main directory. Overrides environment
        variable.'''
    )
    parser.add_argument(
        '--gem5-ckpoint-path',
        help='''Root directory for execution checkpoints. Overrides
        environment variable.'''
    )
    parser.add_argument(
        '--m5out-path',
        help='''Root directory for the generated output. Overrides
        environment variable.'''
    )
    parser.add_argument(
        '-N',
        '--num-jobs',
        default=4,
        help='''Max number of simulation jobs allowed to be running in
        parallel. Overrides environment variable.'''
    )
    parser.add_argument(
        '--benchmarks-path',
        help='''Root directory for the benchmarks. Overrides environment
        variable.'''
    )

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

    return parser.parse_args()


def get_paths(args):
    """Get gem5 paths, from environment or cli arguments."""
    paths = {}

    if 
    elif 'M5_PATH' in os.environ:
        paths['M5_PATH'] = 'M5_PATH'

    return paths


def run_fs(paths, args_gem5, args_config):
    """Run gem5 with the given arguments."""
    args = [paths['gem5_path']] + args_gem5 + [paths['config']] + args_config
    subprocess.run()


def main():
    print("Done!")


if __name__ == "__main__":
    main()
