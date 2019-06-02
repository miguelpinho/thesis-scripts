#!/usr/bin/env python3

import argparse
import datetime
import subprocess
import os

def get_arguments:
    """Parse rungem5 arguments."""
    parser = argparse.ArgumentParser(description='Run gem5 full-system.')
    subparsers = parser.add_subparsers(title='action', help='action to perform')

    # generic options
    parser.add_argument('env_file', help="")
    parser.add_argument('gem5_path')
    parser.add_argument('m5out_path')

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


def get_paths():
    """Get gem5 paths, from environment or cli arguments."""

def run_fs():
    """Run gem5 with the given arguments."""
    args_gem5 = []
    args_config = []
    
    args = [gem5_path] + args_gem5 + [config_path] + args_config
    subprocess.run()


def main():
    print("Done!")


if __name__ == "__main__":
    main()
