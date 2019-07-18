#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Util and module for running gem5 simulations in system-call emulation mode.
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path
from datetime import datetime

from dotenv import load_dotenv


def get_arguments():
    """Parse rungem5 arguments."""
    parser = argparse.ArgumentParser(
        description='Run gem5 system-call emulation mode.')

    # generic options
    # env
    parser.add_argument(
        '--env-file',
        default=argparse.SUPPRESS,
        help='''script file frow where to load environment variables'''
    )
    parser.add_argument(
        '--gem5-path',
        default=argparse.SUPPRESS,
        help='''path to the gem5 main directory. Overrides environment
        variable'''
    )
    parser.add_argument(
        '--m5out-path',
        default=argparse.SUPPRESS,
        help='''root directory for the generated output. Overrides
        environment variable'''
    )
    # gem5 options
    parser.add_argument(
        '--arch',
        choices=('ARM', 'X86', 'ALPHA', 'SPARC', 'RISCV'),
        default='ARM',
        help='''cpu architecture'''
    )
    parser.add_argument(
        '--binary-mode',
        choices=('debug', 'opt', 'fast', 'prof', 'perf'),
        default='opt',
        help='''gem5 binary mode'''
    )
    parser.add_argument(
        '--out-folder',
        default=argparse.SUPPRESS,
        help='''m5out sub-folder name. Overrides default folder for action''',
    )
    parser.add_argument(
        '--wildcard-gem5',
        default=None,
        help='''wildcard arguments to be passed to gem5 binary'''
    )
    # simulation options
    parser.add_argument(
        '-N',
        '--sim-jobs',
        type=int,
        default=4,
        help='''max number of simulation jobs allowed to be running in
        parallel. Overrides environment variable''',
    )
    parser.add_argument(
        '--no-caches',
        action="store_true",
        default=False,
        help='''do not use l1 and l2 caches'''
    )
    parser.add_argument(
        '--fast-cpu',
        action="store_true",
        default=False,
        help='''use AtomicSimpleCPU as the main cpu-type'''
    )
    # binary to run in simulation
    parser.add_argument(
        '--cmd',
        '-c',
        default=None,
        help='''binary to run in system-call emulation mode'''
    )

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

    # Environment paths
    # (description, arg, env, path)
    req_paths = [
        ("gem5 root dir", 'gem5_path', 'GEM5_PATH', 'GEM5'),
        ("gem5 output root dir", 'm5out_path', 'M5OUT_PATH', 'M5OUT')
    ]

    dic_args = vars(args)
    for p in req_paths:
        if p[1] in args:
            path = Path(dic_args[p[1]])
        elif p[2] in os.environ:
            path = Path(os.environ[p[2]])
        else:
            print("No path for '{}' was provided. Use option '--{}' or env "
                  "variable '{}'.".format(p[0], p[1], p[2]))
            sys.exit()

        if not path.is_dir():
            print("Invalid path for '{}': '{}'.".format(p[0], path))
            sys.exit()
        paths[p[3]] = path

    # Output path
    paths['OUT_PATH'] = get_folder_path(args, paths) / get_run_tag(args)

    return paths


def get_folder_path(args, paths):
    """Return the tag for the output folder tree."""
    date_tag = datetime.utcnow().strftime("%d-%b-%Y").lower()

    output_path = Path(paths['M5OUT']) / date_tag
    return output_path


def get_run_tag(args):
    """Returns the tag for this run's output."""
    if "out_folder" in args:
        return args.out_folder

    # SE task
    task_tag = 'se'

    # Timestamp
    time_tag = datetime.utcnow().strftime("%Hh%Mm")

    return task_tag + '_' + time_tag


def get_gem5_bin(args, paths):
    bin_name = "gem5.{}".format(args.binary_mode)
    arch = args.arch

    bin_path = paths['GEM5'] / 'build' / arch / bin_name

    if not bin_path.exists():
        print("Invalid gem5 binary path: '{}'.".format(bin_path))
        sys.exit()

    return bin_path


def get_gem5_args(args, paths):
    """Returns the list of args to be passed to the gem5 binary."""
    args_gem5 = []

    args_gem5.append('--outdir={}'.format(paths['OUT_PATH']))

    if not args.wildcard_gem5 is None:
        wildcards = args.wildcard_gem5.split()
        args_gem5.extend(wildcards)

    return args_gem5


def get_config_args(args, paths):
    """Returns the list of args to be passed to the config script."""
    # TODO: Fix how paths are generated (Path).

    args_config = []

    # caches
    if not args.no_caches:
        args_config.extend(['--caches', '--l2cache'])

    # command
    if args.cmd is not None:
        args_config.append("--cmd={}".format(args.cmd))

    if not args.fast_cpu:
        args_config.append("--cpu-type={}".format('O3_ARM_v7a_3'))
    else:
        args_config.append("--cpu-type={}".format('AtomicSimpleCPU'))

    return args_config


def run_fs(args, paths, bin_gem5, args_gem5, config_script, args_config):
    """Run gem5 with the given arguments."""
    run_args = [str(bin_gem5)] + args_gem5 + [str(config_script)] + args_config

    print('Running command:\n{}'.format(' '.join(run_args)))

    subprocess.run(run_args)


def main():
    args = get_arguments()

    load_env(args)
    paths = get_paths(args)

    print(paths)
    bin_gem5 = get_gem5_bin(args, paths)
    args_gem5 = get_gem5_args(args, paths)
    config_script = paths['GEM5'] / 'configs' / 'example' / 'se.py'
    args_config = get_config_args(args, paths)

    run_fs(args, paths, bin_gem5, args_gem5, config_script, args_config)


if __name__ == "__main__":
    main()
