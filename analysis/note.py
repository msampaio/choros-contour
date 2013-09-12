#!/usr/bin/env python
# -*- coding: utf-8 -*-

import music21
from music21.contour import Contour
from music21.musedata.base40 import pitchToBase40
from music21.interval import notesToInterval, notesToChromatic
import itertools


class Note(object):
    """Class for Note objects."""

    def __init__(self):
        self.name = None
        self.code = None
        self.duration = None
        self.octave = None
        self.offset = None

    def __repr__(self):
        return u"<Note: {0}{1}>".format(self.name, self.octave)


def songNotes(score):
    # For some reason Stream([n for n in score.flat.notes]) accumulate
    # notes in the wrong order, so we append them explicitly.

    stream = music21.stream.Stream()
    for n in score.flat.notes.stripTies():
        if n.isChord:
            stream.append(n[-1])
        else:
            stream.append(n)
    return stream


def makeNote(n):
    note = Note()
    note.name = n.name
    note.code = music21.musedata.base40.pitchToBase40(n)
    note.duration = n.duration.quarterLength
    note.octave = n.octave
    note.offset = n.offset

    return note


def intervalsWithoutDirection(notes):
    size = len(notes)
    pos = zip(range(size-1), range(1, size))
    return [notesToInterval(notes[x], notes[y]).name for x, y in pos]


def intervalsWithDirection(notes):
    # FIXME: m-2, P-4, etc
    size = len(notes)
    pos = zip(range(size-1), range(1, size))
    return [notesToInterval(notes[x], notes[y]).directedName for x, y in pos]


def intervalsWithDirectionSemitones(notes):
    size = len(notes)
    pos = zip(range(size-1), range(1, size))
    return [notesToInterval(notes[x], notes[y]).semitones for x, y in pos]


def durations(notes):
    """Return a sequence of durations of a given sequence of notes."""

    return [note.duration.quarterLength for note in notes]


def splitByBeat(notes):
    """Return a given sequence of notes split by beats."""

    seq = [(n.offset, n) for n in notes]
    return [[x[1] for x in list(lst)] for _, lst in itertools.groupby(seq, lambda x: int(x[0]))]


def beatContents(notes):
    """Return the beat contents of a given sequence of notes in
    quarterLengths."""

    return [[n.duration.quarterLength for n in beat] for beat in splitByBeat(notes)]
