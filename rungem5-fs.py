#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Util and module for running gem5 full-system simulations.
"""

import argparse
import datetime
import subprocess
import os
from pathlib import Path
from dotenv import load_dotenv


def get_arguments():
    """Parse rungem5 arguments."""
    parser = argparse.ArgumentParser(description='Run gem5 full-system.')
    subparsers = parser.add_subparsers(
        title='action', help='action to perform')

    # generic options
    # env
    parser.add_argument(
        '--env-file',
        default=argparse.SUPPRESS,
        help='''Script file frow where to load environment variables.'''
    )
    parser.add_argument(
        '--gem5-path',
        default=argparse.SUPPRESS,
        help='''Path to the gem5 main directory. Overrides environment
        variable.'''
    )
    parser.add_argument(
        '--m5-path',
        default=argparse.SUPPRESS,
        help='''Path to the gem5 full-system files. Overrides environment
        variable.'''
    )
    parser.add_argument(
        '--gem5-ckpoint-path',
        default=argparse.SUPPRESS,
        help='''Root directory for execution checkpoints. Overrides
        environment variable.'''
    )
    parser.add_argument(
        '--m5out-path',
        default=argparse.SUPPRESS,
        help='''Root directory for the generated output. Overrides
        environment variable.'''
    )
    parser.add_argument(
        '-N',
        '--num-jobs',
        default=4,
        help='''Max number of simulation jobs allowed to be running in
        parallel. Overrides environment variable.''',
    )
    parser.add_argument(
        '--benchmarks-path',
        help='''Root directory for the benchmarks. Overrides environment
        variable.'''
    )

    # "boot" action
    parser_boot = subparsers.add_parser('boot', help='boot full-system')

    # "checkpoint" action
    parser_ckpoint = subparsers.add_parser(
        'checkpoint', help='boot, save checkpoints and exit')

    # "restore" action
    parser_restore = subparsers.add_parser(
        'restart', help='restore from checkpoint')

    # "script" action
    parser_script = subparsers.add_parser(
        'script', help='restore and run script')

    # "benchmark" action
    parser_benchmark = subparsers.add_parser(
        'benchmark', help='restore and run available benchmarks')

    return parser.parse_args()


def load_env(args):
    """Loads the .env file, if any was passed or .env is detected."""
    # Passed env_file is priority. Overrides environment vars.
    if "env_file" in args:
        env_path = Path(args.env_file)
        if env_path.exists():
            try:
                load_dotenv(dotenv_path=env_path, override=True)
            except IOError:
                print("Could not open env_file file. Ignoring.")
            else:
                return
        else:
            print("Invalid env_file path. Ignoring.")

    # Next, tries the default .env file. This one does not override.
    env_path = Path('.') / '.env'
    if env_path.exists():
        try:
            load_dotenv(dotenv_path=env_path)
        except:
            pass


def get_paths(args):
    """
    Get gem5 paths, from environment or cli arguments.

    Priorities: cli args > .env arg > environment > default .env
    """
    paths = {}

    # description | arg | env | path
    req_paths = [
        ("gem5 root dir", 'gem5_path', 'GEM5_PATH', 'GEM5'),
        ("full-system files dir", 'm5_path', 'M5_PATH', 'M5'),
        ("gem5 checkpoints dir", 'gem5_ckpoint_path',
         'GEM5_CKPOINT_PATH', 'GEM5_CKPOINT'),
        ("gem5 output root dir", 'm5out_path', 'M5OUT_PATH', 'M5OUT')
    ]

    dic_args = vars(args)

    for p in req_paths:
        if p[1] in args:
            paths[p[3]] = dic_args[p[1]]
        elif p[2] in os.environ:
            paths[p[3]] = os.environ[p[2]]
        else:
            print("No path for '{}' was provided. Use option or env "
                  "variable '{}'.".format(p[0], p[2]))
            pass

    return paths


def run_fs(paths, args_gem5, args_config):
    """Run gem5 with the given arguments."""
    args = [paths['GEM5']] + args_gem5 + \
        [paths['GEM5'] + '/config/fs.py'] + args_config

    print('Running command: {}'.format(' '.join(args)))

    # subprocess.run()


def main():
    args = get_arguments()

    load_env(args)
    paths = get_paths(args)

    print(paths)

    args_gem5 = []
    args_config = []

    run_fs(paths, args_gem5, args_config)


if __name__ == "__main__":
    main()
