#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import os
import glob


def flatten(seq):
    """Flatten Sequences.

    >>> flatten([[0, 1], [2, 3]])
    [0, 1, 2, 3]
    """

    return [item for sublist in seq for item in sublist]


def sort2(dic):
    return sorted(dic.items(), reverse=True, key=lambda x: x[1])


def percentage(dic):
    """Return a dictionary with percent values"""

    def perc(val, total):
        return val * 100.0 / total

    total = sum(dic.values())
    return {k: perc(v, total) for k, v in dic.items()}


def subplot_base(plots_number):
    maximum = 3
    square = plots_number ** 0.5
    rows_columns = math.ceil(square)
    return int((rows_columns - 1) * 100 + rows_columns * 10)


def __path_without_extension(path):
    """Returns a complete path of a file without extension."""

    directory = os.path.dirname(path)
    basename = os.path.basename(path)
    songfilename = basename.split('.')[0]
    return os.path.join(directory, songfilename)


def filenames_list(collection, extension='phrase'):
    """Returns a list of paths that have .phrase."""

    directory = os.path.join(os.getcwd(), 'choros-corpus', collection)
    phrase_files = glob.glob(os.path.join(directory, "*.{0}".format(extension)))

    return [__path_without_extension(filename) for filename in phrase_files]
