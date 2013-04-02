#!/usr/bin/env python
# -*- coding: utf-8 -*-

import music21
import os
import glob
import pickle
from music21.contour import Contour


class Phrase(object):
    def __init__(self, score='', piece='', composer='', filename='', collection='', number=0, size=0, contour=None, contour_size=0, time_signature=(0, 0)):
        self.score = score
        self.piece = piece
        self.composer = composer
        self.filename = filename
        self.collection = collection
        self.number = number
        self.size = size
        self.contour = contour
        self.contour_size = contour_size
        self.time_signature = time_signature

    def __repr__(self):
        return "<Phrase: {0}. {1}:{2}>".format(self.piece, self.collection, self.number)


def m21_data(x_name):
    """Returns Music21 data (flatten stream object, piece name,
    composer) and collection from a given xml file path.
    """

    song = music21.parse(x_name)
    piece = song.metadata.title
    composer = song.metadata.composer
    collection = os.path.basename(os.path.dirname(x_name))
    flatten_obj = song.flat.notesAndRests
    time_signature_obj = song.flat.getElementsByClass(music21.meter.TimeSignature)[0]
    time_signature = time_signature_obj.numerator, time_signature_obj.denominator

    return flatten_obj, piece, composer, collection, time_signature

def phrase_locations_parser(p_name):
    """Returns a list with event numbers of phrases from a .phrase
    file path.
    """

    with open(p_name) as pfile:
        return [[int(n) for n in loc.split()] for loc in pfile.readlines()]

def split_phrase(flatten_obj, phrase_locations):
    """Returns a list of phrases from a given music21 flatten score
    object, and a list of phrase locations.
    """
    
    return [flatten_obj[beg - 1:end] for beg, end in phrase_locations]


def color_phrase_obj(basename):
    """Return a music21 stream object with colored first and last
    phrase notes."""

    p_name = basename + '.phrase'
    x_name = basename + '.xml'

    song = music21.parse(x_name)
    measures = song.parts[0].getElementsByClass('Measure')
    locations = phrase_locations_parser(p_name)

    beginning = []
    ending =[]

    for loc in locations:
        beginning.append(loc[0])
        ending.append(loc[1])

    n = 0
    for measure in measures:
        events = measure.notesAndRests
        for event in events:
            n += 1
            if n in beginning:
                event.color = 'blue'
            elif n in ending:
                event.color = 'red'

    return song


def make_phrase_obj(basename, music21_obj=True):
    """Returns a list of Phrase objects with each phrase of a given
    file path. The file path must not have extension.
    """

    p_name = basename + '.phrase'
    x_name = basename + '.xml'
    flatten_obj, piece, composer, collection, time_signature = m21_data(x_name)
    phrase_locations = phrase_locations_parser(p_name)
    phrases_obj = split_phrase(flatten_obj, phrase_locations)
    phrases_number = len(phrases_obj)
    print "Making {0} phrases of {1}".format(phrases_number, piece)

    result = []
    for number, phr in enumerate(phrases_obj):
        number = number + 1
        size = len(phr)
        contour = Contour(phr)
        contour_size = len(contour)

        # option to create Phrase object without music21 attribute to
        # save in pickle
        if not music21_obj:
            phr = ''

        result.append(Phrase(phr, piece, composer, x_name, collection, number, size, contour, contour_size, time_signature))

    return result


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


def make_phrase_collection(collection, music21_obj=True):
    """Returns a list of phrases objects separated by piece.
    """

    files = filenames_list(collection)
    return [make_phrase_obj(f, music21_obj) for f in files]


def save_pickle(filename, data):
    with open(os.path.join("data", filename), 'w') as fileobj:
        pickle.dump(data, fileobj)


def load_pickle(filename):
    with open(os.path.join("data", filename)) as fileobj:
        return pickle.load(fileobj)
