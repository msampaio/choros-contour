#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import Counter


def durations(notesSeq):
    """Return a sequence of durations of a given sequence of notes."""

    return [note.duration for note in notesSeq]


def segmentDurations(seg):
    """Return a sequence of durations of a given Segment Object."""

    return durations(seg.notes)


def focalPointProportion(seg):
    """Return the offset proportion of ocurrence of the segment
    highest note. If there is more than one highest note, the first
    one is preferred."""

    highestNoteOffset = max(seg.notes, key=lambda n: n.code).offset
    totalLength = seg.totalLength

    return highestNoteOffset / totalLength


def splitByBeat(score, durations=True, count=True):
    def aux(sequence, ind, i):
        return tuple(sequence[ind[i]:ind[i + 1]])

    def noteOrRest(event):
        if event.isNote:
            string = 'note'
        else:
            string = 'rest'

        return string, event.quarterLength

    flatten = score.flat.notesAndRests
    quarterLengthSeq = []
    ind = []
    n = 0

    for el in flatten:
        beat = el.beat
        if beat % 1 == 0:
            ind.append(n)
        n += 1

    ind.append(len(flatten))
    split = []
    durationsSeq = []

    for i in range(len(ind) - 1):
        notes = aux(flatten, ind, i)
        split.append(notes)
        if durations:
            durationsSeq.append(tuple([noteOrRest(note) for note in notes]))

    if durations:
        split = durationsSeq

    if count:
        split = Counter(split)

    return split
