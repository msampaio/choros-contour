#!/usr/bin/env python
# -*- coding: utf-8 -*-

import music21
from music21.contour import Contour
import song
import _utils

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


def phrase_locations_parser(phrase_name):
    """Returns a list with event numbers of phrases from a .phrase
    file path.
    """

    with open(phrase_name) as pfile:
        return [[int(n) for n in loc.split()] for loc in pfile.readlines()]

def split_phrase(flatten_obj, phrase_locations):
    """Returns a list of phrases from a given music21 flatten score
    object, and a list of phrase locations.
    """
    
    return [flatten_obj[beg - 1:end] for beg, end in phrase_locations]


def color_phrase_obj(basename):
    """Return a music21 stream object with colored first and last
    phrase notes."""

    phrase_name = basename + '.phrase'
    xml_name = basename + '.xml'

    song = music21.parse(xml_name)
    measures = song.parts[0].getElementsByClass('Measure')
    locations = phrase_locations_parser(phrase_name)

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

    phrase_name = basename + '.phrase'
    xml_name = basename + '.xml'
    flatten_obj, piece, composer, collection, time_signature = song.m21_data(xml_name)
    phrase_locations = phrase_locations_parser(phrase_name)
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

        result.append(Phrase(phr, piece, composer, xml_name, collection, number, size, contour, contour_size, time_signature))

    return result


def make_phrase_collection(collection, music21_obj=True):
    """Returns a list of phrases objects separated by piece.
    """

    files = _utils.filenames_list(collection)
    return [make_phrase_obj(f, music21_obj) for f in files]
