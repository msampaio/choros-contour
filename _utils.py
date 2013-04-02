#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import glob


def flatten(seq):
    """Flatten Sequences.

    >>> flatten([[0, 1], [2, 3]])
    [0, 1, 2, 3]
    """

    return [item for sublist in seq for item in sublist]




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
