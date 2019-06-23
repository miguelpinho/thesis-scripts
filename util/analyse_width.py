#!/usr/bin/env python3

import sys
import argparse
import numpy as np
from pathlib import Path

"""
Util and module for analysing the width distribution of a data set.
"""


def get_signed_width(val):
    val = int(val)
    if val < 0:
        return val.bit_length()
    else:
        return val.bit_length() + 1


def get_unsigned_width(val):
    val = int(val)
    return val.bit_length()


def main():
    data = np.genfromtxt('normal_mu10_s10_n100_seed777733.csv', dtype=int)

    width = np.array(list(map(get_signed_width, data)))

    print(width)


if __name__ == "__main__":
    main()
