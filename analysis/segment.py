#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _utils
import idcode
import parse


class Segment(object):
    """Class for segment objects."""

    def __init__(self):

        self.source = None

        self.score = None
        self.timeSignature = None
        self.meter = None
        self.ambitus = None
        self.pickup = None
        self.measuresNumber = None
        self.totalLength = None

        self.contour = None
        self.contourPrime = None
        self.contourSize = None

        self.notes = None
        self.intervals = None
        self.intervalsWithDirection = None
        self.firstInterval = None
        self.lastInterval = None

        self.durations = None
        self.beatContents = None

        self.typeof = None
        self.orderNumber = None

        self.initialEvent = None
        self.finalEvent = None

    def __repr__(self):
        title = self.source.piece.title
        composer = self.source.piece.makeComposersString()
        return "<Segment {0}: {1} ({2})>".format(self.orderNumber, title, composer)


def makeSegment(sourceObj, savePickle=False):
    """Return a segment object from a given idCode string."""

    if not sourceObj.score:
        sourceObj.makeScore()
    sourceObj = parse.getInfoAboutSource(sourceObj)

    segments = []

    if sourceObj.formSeq:
        for dic in sourceObj.formSeq:
            typeof = dic['typeof']
            if typeof == 'Phrase':
                orderNumber = dic['number']
                initial = dic['initial']
                final = dic['final']

                seg = Segment()
                seg.source = sourceObj
                seg.orderNumber = orderNumber
                seg.typeof = typeof
                seg.initial = initial
                seg.final = final

                print '. Making object {0}'.format(seg)
                seg.score = sourceObj.getExcerpt(initial, final)
                seg = parse.getInfoAboutSegment(seg)
                if savePickle:
                    seg.score = None
                segments.append(seg)
    else:
        print sourceObj
    if savePickle:
        sourceObj.score = None
    return segments
