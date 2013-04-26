#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import os
import glob
import unicodedata
from PIL import Image, ImageChops


def flatten(seq):
    """Flatten Sequences.

    >>> flatten([[0, 1], [2, 3]])
    [0, 1, 2, 3]
    """

    return [item for sublist in seq for item in sublist]


def sort2(dic):
    """Return a sorted sequence from a dictionary organized by the dictionary values."""

    return sorted(dic.items(), reverse=True, key=lambda x: x[1])


def percentual(seq):
    """Return a sequence with percentual values."""

    total = sum(seq)
    return [(el * 100 / float(total)) for el in seq]


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


def filenames_list(collection, extension='form'):
    """Returns a list of paths that have .form."""

    directory = os.path.join(os.getcwd(), 'choros-corpus', collection)
    phrase_files = glob.glob(os.path.join(directory, "*.{0}".format(extension)))

    return [filename.strip(extension) + 'xml' for filename in phrase_files]


def filename_exclusion(path, exclusions=['.DS_Store', '.git', 'README.md']):
    """Return a sequence of files from a path without the files given
    in exclusions sequence."""

    files = os.listdir(path)
    for ex in exclusions:
        if ex in files:
            files.remove(ex)
    return files


def mkdir(path):
    """Make a path of a given path, if it doesn't exist."""

    if not os.path.exists(path):
        os.mkdir(path)


def unicode_normalize(string):
    """Return a normalized string. It's useful to process filenames
    with special characters."""

    new_string = unicodedata.normalize('NFKD', unicode(string)).encode('ascii', 'ignore')
    return new_string.replace(',', '').replace('?', '')


def group_minorities(dic, percentage=0.05):
    """Return a given dictionary of values, such as {'a': 2, 'b': 4}
    with the keys with the smallest values grouped as 'Others' key.
    The percentage argument defines how small these values must be to
    be grouped."""

    total = sum(dic.viewvalues())
    smallest = total * percentage
    minors = 0
    for k, v in dic.items():
        if v <= smallest:
            minors += v
            dic.pop(k)
    if minors != 0:
        dic['Others'] = minors
    return dic


def image_trim(filename):
    """Save a given image cropped and trimmed. It's useful to remove
    Lilypond tagline and to eliminate blank paper area from the
    image."""

    im = Image.open(filename)
    im = im.crop((0, 0, 776, 1000))
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    bbox = diff.getbbox()
    if bbox:
        im = im.crop(bbox)
        im.save(filename)


def remove_endline(string):
    """Return a given string without new line or crlf."""

    return string.strip('\n').strip('\r')
