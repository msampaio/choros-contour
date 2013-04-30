#!/usr/bin/env python
# -*- coding: utf-8 -*-

import music21
import _utils
import retrieval
import song


def _aux_getBy(segments, save):
    allseg = getSegmentsData(segments)
    allseg.segments = segments
    allseg.segments_number = len(allseg.segments)
    allseg.save = save
    return allseg


class AllSegments(object):
    """Class for a set of Segment objects. This class has attributes
    and methods to return information about Segment objects
    parameters."""

    def __init__(self):
        self.save = None
        self.segments = None
        self.segments_number = None

        self.allComposers = None
        self.allTitles = None
        self.allCollections = None
        self.allContours = None
        self.allContourSizes = None
        self.allContourPrimes = None
        self.allAmbitus = None
        self.allTimeSignatures = None
        self.allMeters = None
        self.allFilenames = None

    def __repr__(self):
        return "<AllSegments: {0} segments>".format(self.segments_number)

    def getByIndex(self, index):
        """Return a Segment object by a given index number."""

        return self.segments[index]

    def getByComposer(self, composer):
        """Return a new AllSegment object with all Segment objects
        with a given composer as attribute."""

        return _aux_getBy([seg for seg in self.segments if seg.composer == composer], self.save)

    def getByTitle(self, title):
        """Return a new AllSegment object with all Segment objects
        with a given song title as attribute."""

        return _aux_getBy([seg for seg in self.segments if seg.title == title], self.save)

    def getByAmbitus(self, ambitus):
        """Return a new AllSegment object with all Segment objects
        with a given ambitus value as attribute."""

        return _aux_getBy([seg for seg in self.segments if seg.ambitus == ambitus], self.save)

    def getByContourPrime(self, contour_prime):
        """Return a new AllSegment object with all Segment objects
        with a given Contour Prime value as attribute."""

        return _aux_getBy([seg for seg in self.segments if seg.contour_prime == contour_prime], self.save)

    def getByPickup(self, pickup=True):
        """Return a new AllSegment object with all Segment objects
        with pickup measure."""

        return _aux_getBy([seg for seg in self.segments if seg.pickup == pickup], self.save)


def getSegmentsData(SegmentsList):
    """Return a dictionary with the data raised in Segment objects."""

    def getData(SegmentsList, attrib):
        s = set()
        for SegmentObj in SegmentsList:
            value = getattr(SegmentObj, attrib)
            if type(value) == music21.contour.contour.Contour:
                value = tuple(value)
                s.add(value)
                r = [music21.contour.contour.Contour(cseg) for cseg in sorted(s)]
            else:
                s.add(value)
                r = sorted(s)
        # FIXME: local variable 'r' referenced before assignment
        return r

    allseg = AllSegments()
    allseg.allComposers = getData(SegmentsList, 'composer')
    allseg.allTitles = getData(SegmentsList, 'title')
    allseg.allCollections = getData(SegmentsList, 'collection')
    allseg.allContours = getData(SegmentsList, 'contour')
    allseg.allContourSizes = getData(SegmentsList, 'contour_size')
    allseg.allContourPrimes = getData(SegmentsList, 'contour_prime')
    allseg.allAmbitus = getData(SegmentsList, 'ambitus')
    allseg.allTimeSignatures = getData(SegmentsList, 'time_signature')
    allseg.allMeters = getData(SegmentsList, 'meter')
    allseg.allFilenames = getData(SegmentsList, 'filename')

    return allseg

def makeAllSegments(save=False):
    """Return an AllSegment object with all Segment objects saved in a
    pickle or in available collections."""

    SegmentsList = []
    songs = retrieval.load_pickle('songs')
    if save:
        songs = retrieval.load_pickle('songs')
    else:
        songs = song.makeSongAllCollections(save)
    for s in songs:
        SegmentsList.extend(s.segments)

    allseg = getSegmentsData(SegmentsList)
    allseg.segments = SegmentsList
    allseg.segments_number = len(allseg.segments)
    allseg.save = save
    return allseg
