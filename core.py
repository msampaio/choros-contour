#!/usr/bin/env python
# -*- coding: utf-8 -*-

import music21
import os
from music21.contour import Contour


class Phrase(object):
    def __init__(self, score, piece='', composer='', filename='', collection='', number=0, size=0, contour=None, contour_size=0):
        self.score = score
        self.piece = piece
        self.composer = composer
        self.filename = filename
        self.collection = collection
        self.number = number
        self.size = size
        self.contour = contour
        self.contour_size = contour_size

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
    return flatten_obj, piece, composer, collection

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


def make_phrase_obj(basename):
    """Returns a list of Phrase objects with each phrase of a given
    file path. The file path must not have extension.
    """

    p_name = basename + '.phrase'
    x_name = basename + '.xml'
    flatten_obj, piece, composer, collection = m21_data(x_name)
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
        result.append(Phrase(phr, piece, composer, x_name, collection, number, size, contour, contour_size))

    return result
