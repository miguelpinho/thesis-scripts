# Thesis scripts

This repository includes a set of scripts for automating my thesis experimental
tasks, namely:

-   running a modified full-system gem5 version;
-   parsing and ploting run metrics;
-   (TODO) performing a power/energy impact analysis using McPAT.

## Contents

-   `rungem5-fs.py`: a wrapper script for running full-system gem5 simulations
    with different configurations;
-   `rungem5-se.py`: a similar script for system call emulation mode;
-   `env/`: sample environment path files, with all the paths needed to run gem5
    simulations (used by `rungem5-fs.py` and `rungem5-se.py`);
-   `sim-scripts/`: collection of gem5 full-system run scripts for a variety of
    public and custom benchmarks;
-   `o3-configs/`: set of O3CPU ARMv8 configurations used for my thesis
    experimental work;
-   `mcpat-templates`: corresponding McPAT templates for these OoO ARMv8 CPU
    configurations;
-   `util/`:
    -   `util/disk/`: utility scripts for (un)mounting and "chrooting"
        full-system disk images;
    -   `util/analysis/`: collection of scripts for parsing gem5 output metrics
        and plotting analysis graphs;
    -   `util/gen_data.py`: a script for generating an integer dataset following
        a random probabilty distribution;
    -   `util/analysis_width.py`: a script for analysing the bit-width
        distribution of an integer dataset.

## Benchmark Scripts

-   Splash-2 benchmarks (most of them);
-   Some PARSEC-3.0 benchmarks;
-   At least two SPEC2006 (probably several more);
-   Custom thesis kernels and mini-apps.
