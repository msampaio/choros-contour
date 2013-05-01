#!/usr/bin/env python
# -*- coding: utf-8 -*-

import music21
from music21.contour import Contour
from music21.musedata.base40 import pitchToBase40
from music21.interval import notesToInterval, notesToChromatic

class Note(object):
    def __init__(self):
        self.name = None
        self.code = None
        self.duration = None
        self.octave = None

    def __repr__(self):
        return u"<Note: {0}{1}>".format(self.name, self.octave)


def song_notes(score):
    # For some reason Stream([n for n in score.flat.notes]) accumulate
    # notes in the wrong order, so we append them explicitly.

    stream = music21.stream.Stream()
    for n in score.flat.notes.stripTies():
        if n.isChord:
            stream.append(n[-1])
        else:
            stream.append(n)
    return stream


def make_note(n):
    note = Note()
    note.name = n.name
    note.code = music21.musedata.base40.pitchToBase40(n)
    note.duration = n.duration.quarterLength
    note.octave = n.octave
    return note


def intervals_without_direction(notes):
    size = len(notes)
    pos = zip(range(size-1), range(1, size))
    return [notesToInterval(notes[x], notes[y]).name for x, y in pos]


def intervals_with_direction(notes):
    size = len(notes)
    pos = zip(range(size-1), range(1, size))
    return [notesToInterval(notes[x], notes[y]).directedName for x, y in pos]


def intervals_with_direction_semitones(notes):
    size = len(notes)
    pos = zip(range(size-1), range(1, size))
    return [notesToInterval(notes[x], notes[y]).semitones for x, y in pos]
