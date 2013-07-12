#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import os
import glob
import unicodedata
from PIL import Image, ImageChops
from collections import Counter
import itertools


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

    return [filename.replace(extension, 'xml') for filename in phrase_files]


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
    return new_string.replace(',', '').replace('?', '').replace('(', '').replace(')', '')


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

    return string.replace('\n', '').replace('\r', '')


def get_filename(collection_number, song_number, path='choros-corpus'):
    """Return absolute filename of a given collection and song numbers."""

    collection = filename_exclusion(path)[collection_number]
    print collection
    files = filenames_list(collection, 'xml')
    for f in files:
        basename = os.path.basename(f)
        number = int(basename.split()[0])
        if number == song_number:
            return f


def count_segments(AllSegmentsObj, attrib):
    return Counter((getattr(seg, attrib) for seg in AllSegmentsObj.segments))


def dicValueInsertion(dic, key, value):
    """Return a given value only if it's not the key value of a given
    dictionary."""

    if key in dic:
        return dic[key]
    else:
        return value


def makeDataCoordSequence(seq):
    newSeq = sorted(percentage(Counter(seq)).items())
    return [[x[1] for x in newSeq], [y[0] for y in newSeq]]


def makeAttribCoordSequence(AllSegmentsObj, attrib, topComposers):
    def aux(AllSegmentsObj, attrib, composer):
        if composer == 'All composers':
            counted = count_segments(AllSegmentsObj, attrib)
        else:
            counted = count_segments(AllSegmentsObj.getByComposer(composer), attrib)
        return [counted.values(), counted.keys()]

    allAndTopComposers = flatten([['All composers'], topComposers])

    return [aux(AllSegmentsObj, attrib, composer) for composer in allAndTopComposers]


def groupby(sequence, index):
    """Group a given sequence of tuples by a given index value.

    >>> groupby([(1, 1), (1, 2), (2, 3), (3, 3)])
    [[(1, 1), (1, 2)], [(2, 3), (3, 3)]]
    """
    return [list(g) for k, g in itertools.groupby(sequence, key=lambda x: x[index])]


def splitTupleSequence(triTupleSequence, index=1):
    """Return a group of tuples grouped by an index. It assumes that
    the tuple's second element value is restarted when the first
    changes.

    >>> seq = [(1, 1, 1), (1, 1, 2), (2, 1, 3), (2, 1, 4), (3, 1, 5), (3,
    1, 6), (4, 1, 7), (4, 1, 8), (5, 1, 9), (5, 1, 10), (6, 1, 11),
    (6, 1, 12), (7, 1, 13), (7, 1, 14), (8, 1, 15), (8, 1, 16), (9, 1,
    17), (9, 1, 18), (10, 1, 19), (10, 1, 20), (11, 1, 21), (11, 1,
    22)]
    >>> splitTupleSequence(seq, 1)
    [[(1, 1, 1), (1, 1, 2)], [(2, 1, 3), (2, 1, 4)], [(3, 1, 5), (3,
    1, 6)], [(4, 1, 7), (4, 1, 8)], [(5, 1, 9), (5, 1, 10)], [(6, 1,
    11), (6, 1, 12)], [(7, 1, 13), (7, 1, 14)], [(8, 1, 15), (8, 1,
    16)], [(9, 1, 17), (9, 1, 18)], [(10, 1, 19), (10, 1, 20)], [(11,
    1, 21), (11, 1, 22)]]
    """

    byFirst = groupby(triTupleSequence, 0)
    if index == 0:
        return byFirst
    else:
        bySecond = []
        for tupleSeq in byFirst:
            if not tupleSeq[0][1] == 0:
                bySecond.extend(groupby(tupleSeq, 1))
        return bySecond


def composerSegments(allSegmentsObj, composer):
    if composer == 'All Composers':
        composerSegments = allSegmentsObj.segments
    else:
        composerSegments = allSegmentsObj.getByComposer(composer).segments

    return composerSegments
