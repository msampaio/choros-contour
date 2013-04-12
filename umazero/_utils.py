#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import os
import glob
import data
import song
import unicodedata


def flatten(seq):
    """Flatten Sequences.

    >>> flatten([[0, 1], [2, 3]])
    [0, 1, 2, 3]
    """

    return [item for sublist in seq for item in sublist]


def sort2(dic):
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


def collections_list(path):
    exclusion = ['.DS_Store', '.git', 'README.md']
    collections = os.listdir(path)
    for el in exclusion:
        try:
            collections.remove(el)
        except:
            print 'The file {0} is not in path {1}'.format(el, path)
    return collections


def mkdir(directory):
    if not os.path.exists(directory):
        os.mkdir(directory)


def make_collection_dict(path='choros-corpus'):
    collection_dict = {}
    for collection in collections_list(path):
        try:
            collection_dict[collection] = data.load_pickle(collection)
        except:
            print "There is no pickle file for collection {0}".format(collection)

    return collection_dict


def make_composer_dict(path='choros-corpus'):
    phrases = []
    for collection in collections_list(path):
        try:
            phrases.extend(flatten(data.load_pickle(collection)))
        except:
            print "There is no pickle file for collection {0}".format(collection)

    composer_dict = {}
    for phrase in phrases:
        composer = phrase.composer
        if not composer in composer_dict:
            composer_dict[composer] = []
        composer_dict[composer].append(phrase)

    return composer_dict


def count_songs_from_phrases(phrases):
    size = len(phrases)
    songnames = []
    for n, phr in enumerate(phrases):
        print "Processing phrase {0} of {1}".format(n, size)
        songname = phr.title
        if songname not in songnames:
            songnames.append(songname)
    return len(songnames)


def unicode_normalize(string):
    return unicodedata.normalize('NFKD', unicode(string)).encode('ascii', 'ignore')


def group_minorities(data, percentage=0.05):
    total = sum(data.viewvalues())
    smallest = total * percentage
    minors = 0
    for k, v in data.items():
        if v <= smallest:
            minors += v
            data.pop(k)
    if minors != 0:
        data['Others'] = minors
    return data
