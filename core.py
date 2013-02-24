#!/usr/bin/env python
# -*- coding: utf-8 -*-

import music21
import os
from music21.contour import Contour


class Phrase(object):
    def __init__(self, piece='', composer='', filename='', collection='', number=0, size=0, contour=None, contour_size=0, lily=''):
        self.piece = piece
        self.composer = composer
        self.filename = filename
        self.collection = collection
        self.number = number
        self.size = size
        self.contour = contour
        self.contour_size = contour_size
        self.lily = lily

    def __repr__(self):
        return "<Phrase: {0}. {1}:{2}>".format(self.piece, self.collection, self.number)


def split_phrases(basename, flatten_song):
    with open(basename + '.phrase') as pf:
        phrase_loc = [[int(n) for n in loc.split()] for loc in pf.readlines()]
    return [flatten_song[beg - 1:end] for beg, end in phrase_loc]


def make_phrases(basename):
    """Create Pharse objects from a given xml file:

    >>> make_phrases('file.xml')
    """

    song = music21.parse(basename + '.xml')

    piece = song.metadata.title
    composer = song.metadata.composer
    # FIXME: improve collection and filename retrieval approach
    collection, filename = basename.split('/')[-2:]

    print "Making phrase of {0}".format(piece)
    flatten_song = song.flat.notesAndRests
    phrases = split_phrases(basename, flatten_song)

    result = []
    for number, phr in enumerate(phrases):
        number = number + 1
        size = len(phr)
        # insert lily
        contour = Contour(phr)
        contour_size = len(contour)
        result.append(Phrase(piece, composer, filename, collection, number, size, contour, contour_size))

    return result


def files_list(directory=os.path.join(os.getcwd(), 'choros-corpus', 'O Melhor de Pixinguinha')):
    return [os.path.join(directory, f.split('.phrase')[0]) for f in os.listdir(directory) if f.endswith('.phrase')]
