#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Util and module for running gem5 full-system simulations.
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path
from datetime import datetime

from dotenv import load_dotenv


DEFAULT_SIM_JOBS = 4


def get_arguments():
    """Parse rungem5 arguments."""
    parser = argparse.ArgumentParser(description='Run gem5 full-system.')
    subparsers = parser.add_subparsers(
        title='action',
        dest='action',
        help='action to perform'
    )
    subparsers.required = True

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
        '--m5-path',
        default=argparse.SUPPRESS,
        help='''path to the gem5 full-system files. Overrides environment
        variable'''
    )
    parser.add_argument(
        '--gem5-ckpoint-path',
        default=argparse.SUPPRESS,
        help='''root directory for execution checkpoints. Overrides
        environment variable'''
    )
    parser.add_argument(
        '--ckpoints-tree',
        action="store_true",
        default=False,
        help='''use scriptset folder tree in the ckpoint dir'''
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
    parser.add_argument(
        '--wildcard-config',
        default=None,
        help='''wildcard arguments to be passed to the python config script'''
    )
    # simulation options
    parser.add_argument(
        '-N',
        '--sim-jobs',
        type=int,
        default=argparse.SUPPRESS,
        help='''max number of simulation jobs allowed to be running in
        parallel. Overrides environment variable''',
    )
    parser.add_argument(
        '--nodes-file',
        default=argparse.SUPPRESS,
        help='''for remote parallel processing, provides the file with the
        ssh hosts''',
    )
    parser.add_argument(
        '-C',
        '--cpu-cores',
        type=int,
        default=1,
        help='''number of cores in each simulated cpu'''
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
    parser.add_argument(
        '--cpu-type',
        default="O3_ARM_v7a_3",
        help='''type of cpu to use'''
    )
    parser.add_argument(
        '--disk-image-file',
        default='ubuntu-14.04.img',
        help='''disk image for the simulation. Should be located in
        $M5_PATH/disks/'''
    )
    parser.add_argument(
        '--run-tag',
        default=None,
        help='''suffix for the output folder generated'''
    )

    # "info" action
    parser_info = subparsers.add_parser(
        'info', help='show the gem5 or config file help')
    parser_info.add_argument(
        'info_option',
        choices=('gem5', 'config'),
        default='gem5',
        nargs='?',
        help='info to show'
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
    parser_script.add_argument(
        'script',
        help='''script to run on boot'''
    )

    # "scriptset" action
    parser_scriptset = subparsers.add_parser(
        'scriptset',
        help='runs several script simulations in parallel'
    )
    parser_scriptset.add_argument(
        'script_set',
        help='''list of scripts to run'''
    )
    parser.add_argument(
        '--runs',
        type=int,
        default=1,
        help='''number of runs for each script'''
    )

    # "benchmark" action
    parser_benchmark = subparsers.add_parser(
        'benchmark',
        help='runs a benchmark suite in parallel'
    )
    parser_benchmark.add_argument(
        'bench',
        choices=('all', 'spec2006', 'parsec3',
                 'splash2', 'apps', 'kernels'),
        help='benchmark suite to run'
    )
    parser_benchmark.add_argument(
        '--workload',
        choices=('test', 'tiny', 'small', 'normal', 'large'),
        default='test',
        help='size of the benchmarks workload'
    )

    return parser.parse_args()


def load_env(args):
    """Loads the .env file, if any was passed or .env is detected."""
    # Passed env_file is priority. Overrides environment vars.
    if "env_file" in args:
        env_path = Path(args.env_file)
        if env_path.exists():
            try:
                load_dotenv(dotenv_path=str(env_path), override=True)
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
        ("full-system files dir", 'm5_path', 'M5_PATH', 'M5'),
        ("gem5 checkpoints dir", 'gem5_ckpoint_path',
         'GEM5_CKPOINT_PATH', 'GEM5_CKPOINT'),
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

    # File paths
    disk_path = paths['M5'] / "disks" / args.disk_image_file
    if not disk_path.is_file():
        print("Invalid path disk image path: {}.".format(disk_path))
        sys.exit()
    paths['DISK'] = disk_path

    # Output path
    paths['OUT_PATH'] = get_folder_path(args, paths) / get_run_tag(args)

    # Benchmark sim-scripts dir
    if args.action == 'benchmark':
        sim_path = Path(__file__).resolve().parent / 'sim-scripts'
        if args.bench == 'kernels':
            bench_dir = sim_path / 'thesis-kernels'
        else:
            print('Unimplemented benchmark: {}.'.format(args.bench))
            sys.exit()

        if not bench_dir.is_dir():
            print('Invalid benchmark dir: {}.'.format(bench_dir))
            sys.exit()

        paths['BENCH_DIR'] = bench_dir

    if args.action == 'scriptset':
        script_set = Path(args.script_set)
        if not script_set.is_file():
            print('Invalid script set file path: {}.'.
                  format(script_set))
        paths['SCRIPTS_DIR'] = script_set.parent
        paths['SCRIPTS_FILE'] = script_set

    return paths


def get_folder_path(args, paths):
    """Return the tag for the output folder tree."""
    date_tag = datetime.utcnow().strftime("%d-%b-%Y").lower()

    output_path = Path(paths['M5OUT']) / date_tag
    return output_path


def get_run_tag(args):
    """Returns the tag for this run's output."""
    if args.action == "info":
        return ""
    elif "out_folder" in args:
        return args.out_folder

    # Number of cpus simulated
    cpus = args.cpu_cores
    cpus_tag = "{}cpu".format(cpus)
    if cpus != 1:
        cpus_tag += "s"

    # Name of the action performed
    # If it was a benchmark, include its name and size
    if args.action == "benchmark":
        task_tag = args.bench + '-' + args.workload
    else:
        task_tag = args.action

    # Timestamp
    time_tag = datetime.utcnow().strftime("%Hh%Mm")

    # Custom tag
    if args.run_tag is None:
        custom_tag = ""
    else:
        custom_tag = "_" + args.run_tag

    return task_tag + '-' + cpus_tag + '_' + time_tag + custom_tag


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
    if args.action == 'info' and args.info_option == 'gem5':
        return ['--help']
    else:
        args_gem5 = []

        if args.action == 'info' and args.info_option == 'config':
            args_gem5.extend(['--redirect-stderr'])
        else:
            args_gem5.extend(['--redirect-stdout', '--redirect-stderr'])

        if args.action == 'benchmark' or args.action == 'scriptset':
            args_gem5.append(
                '--outdir={}'.format(paths['OUT_PATH'] / r'{1.}_{2}'))
        else:
            args_gem5.append('--outdir={}'.format(paths['OUT_PATH']))

        if not args.wildcard_gem5 is None:
            wildcards = args.wildcard_gem5.split()
            args_gem5.extend(wildcards)

    return args_gem5


def get_config_args(args, paths):
    """Returns the list of args to be passed to the config script."""
    # TODO: Fix how paths are generated (Path).
    if args.action == 'info':
        if args.info_option == 'config':
            return ['--help']

    args_config = []

    num_cpus = args.cpu_cores
    arch = args.arch

    args_config.append('--num-cpus={}'.format(num_cpus))

    # full-system files
    if arch == 'ARM':
        # architecure specific files
        args_config.append(
            '--disk-image={}'.format(paths['DISK']))

        args_config.append('--machine-type=VExpress_GEM5_V1')
        args_config.append(
            '--kernel={}/binaries/vmlinux.vexpress_gem5_v1_64'.format(paths['M5']))

        if num_cpus == 1:
            # number of cpus specific config
            args_config.append(
                '--dtb-filename={}/binaries/armv8_gem5_v1_1cpu.dtb'.format(paths['M5']))
        else:
            print("Unsupported number of simulation cpus: '{}'.".format(num_cpus))
            sys.exit()
    else:
        print("Unsupported architecture: '{}'.".format(arch))
        sys.exit()

    # caches
    if not args.no_caches:
        args_config.extend(['--caches', '--l2cache'])

    # action specific
    if args.action == 'checkpoint':
        script = Path.cwd() / "sim-scripts" / "checkpoint.sh"
        args_config.append("--script={}".format(script))
    elif args.action == 'script':
        script = Path(args.script)
        if not script.is_file():
            print('Invalid script path: {}.'.format(args.script_path))
            sys.exit()
        args_config.append("--script={}".format(script))
    elif args.action == 'benchmark':
        args_config.append("--script={}/".format(paths['BENCH_DIR']) + r'{1}')
    elif args.action == 'scriptset':
        args_config.append(
            "--script={}/".format(paths['SCRIPTS_DIR']) + r'{1}')

    if args.action in ['restart', 'script', 'benchmark', 'scriptset']:
        if not args.fast_cpu:
            args_config.append("--cpu-type={}".format(args.cpu_type))
        else:
            args_config.append("--cpu-type={}".format('AtomicSimpleCPU'))

        if args.ckpoints_tree and args.action in ['benchmark', 'scriptset']:
            args_config.append( "--checkpoint-dir={}/{}".format(paths['GEM5_CKPOINT'] / 'fs', r'{1.}'))
        else:
            args_config.append( "--checkpoint-dir={}".format(paths['GEM5_CKPOINT'] / 'fs'))
        args_config.append("--checkpoint-restore={}".format(1))
        args_config.append("--restore-with-cpu={}".format('AtomicSimpleCPU'))

    if not args.wildcard_config is None:
        wildcards = args.wildcard_config.split()
        args_config.extend(wildcards)

    return args_config


def get_sim_jobs(args):
    if 'sim_jobs' in args:
        sim_jobs = args.sim_jobs
    elif 'MACHINE_MAX_JOBS' in os.environ:
        sim_jobs = int(os.environ['MACHINE_MAX_JOBS'])
    else:
        print("The number of jobs was not passed. Using default of {}."
              .format(DEFAULT_SIM_JOBS))
        sim_jobs = DEFAULT_SIM_JOBS

    if sim_jobs < 1:
        print('Invalid number of sim-jobs: {}.'.format(args.runs))
        sys.exit()

    return sim_jobs


def run_fs(args, paths, bin_gem5, args_gem5, config_script, args_config):
    """Run gem5 with the given arguments."""
    run_args = [str(bin_gem5)] + args_gem5 + [str(config_script)] + args_config

    if args.action in ['benchmark', 'scriptset']:
        parallel_options = ['parallel', '--bar']
        if 'nodes_file' in args:
            nodes_file = Path(args.nodes_file)
            if not nodes_file.is_file():
                print('Invalid nodes file: {}.'.format(args.nodes_file))
            parallel_options.extend(['--sshloginfile={}'.format(str(nodes_file)),
                                     '--sshdelay=0.2',
                                     '--env=M5_PATH'])
        else:
            parallel_options.append('--max-procs={}'.format(get_sim_jobs(args)))

        if args.action == 'benchmark':
            bench_txt = paths['BENCH_DIR'] / (args.workload + '.txt')
            if not bench_txt.is_file():
                print('Invalid benchmark list file: {}.'.format(bench_txt))
                sys.exit()
            parallel_args = ['::::', str(bench_txt)]
        elif args.action == 'scriptset':
            parallel_args = ['::::', str(paths['SCRIPTS_FILE']), ':::']
            if args.runs < 1:
                print('Invalid number of runs: {}.'.format(args.runs))
                sys.exit()
            parallel_args.extend([str(n) for n in range(args.runs)])

        run_args = parallel_options + run_args + parallel_args

    print('Running command:\n{}'.format(' '.join(run_args)))

    subprocess.run(run_args)


def main():
    args = get_arguments()

    load_env(args)
    paths = get_paths(args)

    print(paths)
    bin_gem5 = get_gem5_bin(args, paths)
    args_gem5 = get_gem5_args(args, paths)
    config_script = paths['GEM5'] / 'configs' / 'example' / 'fs.py'
    args_config = get_config_args(args, paths)

    run_fs(args, paths, bin_gem5, args_gem5, config_script, args_config)


if __name__ == "__main__":
    main()
