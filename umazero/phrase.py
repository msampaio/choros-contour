#!/usr/bin/env python
# -*- coding: utf-8 -*-

import music21
from music21.contour import Contour
import song
import _utils


class Phrase(object):
    def __init__(self, score=None, title=None, composer=None, filename=None, collection=None, number=None, size=None, contour=None, contour_size=None, time_signature=None, ambitus=None, initial=None, final=None, pickup=None):
        self.score = score
        self.title = title
        self.composer = composer
        self.filename = filename
        self.collection = collection
        self.number = number
        self.size = size
        self.contour = contour
        self.contour_size = contour_size
        self.time_signature = time_signature
        self.ambitus = ambitus
        self.initial = initial
        self.pickup = pickup
        self.final = final

    def __repr__(self):
        return "<Phrase: {0}. {1}:{2}>".format(self.title, self.collection, self.number)

    def show(self, arg=None):
        if self.score:
            self.score.show(arg)

    def make_phrase_score(self):
        if not self.score:
            s = song.make_song(self.filename)
            self.score = s.get_phrase(self.initial, self.final)
        return self


def phrase_locations_parser(phrase_name):
    """Returns a list with event numbers of phrases from a .phrase
    file path.
    """

    def make_location(location):
        return [int(n) for n in location.split()]

    with open(phrase_name) as pfile:
        return [make_location(location) for location in pfile.readlines() if make_location(location)]


def split_phrase(songObj, phrase_locations):
    """Returns a list of phrases from a given music21 flatten score
    object, and a list of phrase locations.
    """

    return [songObj.get_phrase(beg, end) for beg, end in phrase_locations]


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


def make_phrase(basename, music21_obj=True):
    """Returns a list of Phrase objects with each phrase of a given
    file path. The file path must not have extension.
    """

    phrase_name = basename + '.phrase'
    xml_name = basename + '.xml'

    songObj = song.make_song(xml_name)
    title = songObj.title
    composer = songObj.composer
    collection = songObj.collection
    time_signature = songObj.time_signature

    phrase_locations = phrase_locations_parser(phrase_name)
    phrases_obj = split_phrase(songObj, phrase_locations)
    phrases_number = len(phrases_obj)
    print "Making {0} phrases of {1}".format(phrases_number, title)

    result = []
    for number, phr in enumerate(phrases_obj):
        number = number + 1
        size = len(phr)
        contour = Contour(phr)
        contour_size = len(contour)
        ambitus = phr.analyze("ambitus").chromatic.directed
        initial = phr.initial
        final = phr.final
        pickup = phr.pickup

        # option to create Phrase object without music21 attribute to
        # save in pickle
        if not music21_obj:
            phr = None

        result.append(Phrase(phr, title, composer, xml_name, collection, number, size, contour, contour_size, time_signature, ambitus, initial, final, pickup))

    return result


def make_phrase_collection(collection, music21_obj=True):
    """Returns a list of phrases objects separated by piece.
    """

    files = _utils.filenames_list(collection)
    return [make_phrase(f, music21_obj) for f in files]
