#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _utils
import idcode


class Segment():
    """Class for segment objects."""
    
    def __init__(self):

        self.id = None
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

        self.typeof = None
        self.orderNumber = None

        self.initialEvent = None
        self.finalEvent = None

    def __repr__(self):
        title = self.source.piece.title
        composer = self.source.piece.makeComposersString()
        return "<Segment {0}: {1} - ({2}) [{3}]>".format(self.id, title, composer, self.orderNumber)
