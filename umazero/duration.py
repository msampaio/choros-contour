#!/usr/bin/env python
# -*- coding: utf-8 -*-


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
