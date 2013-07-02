#!/usr/bin/env python
# -*- coding: utf-8 -*-


def durations(notesSeq):
    """Return a sequence of durations of a given sequence of notes."""

    return [note.duration for note in notesSeq]


def segmentDurations(seg):
    """Return a sequence of durations of a given Segment Object."""

    return durations(seg.notes)
