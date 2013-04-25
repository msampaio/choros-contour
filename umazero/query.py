#!/usr/bin/env python
# -*- coding: utf-8 -*-

import music21
import _utils
import retrieval
import song


def _aux_getBy(segments, save):
    d = getSegmentsData(segments)
    d['segments'] = segments
    return AllSegments(d, save)


class AllSegments(object):
    """Class for a set of Segment objects. This class has attributes
    and methods to return information about Segment objects
    parameters."""

    def __init__(self, data, save=False):
        self.save = save
        self.segments = data['segments']
        self.segments_number = len(self.segments)

        self.allComposers = data['allComposers']
        self.allTitles = data['allTitles']
        self.allCollections = data['allCollections']
        self.allContours = data['allContours']
        self.allContourSizes = data['allContourSizes']
        self.allContourPrimes = data['allContourPrimes']
        self.allAmbitus = data['allAmbitus']
        self.allTimeSignatures = data['allTimeSignatures']
        self.allMeters = data['allMeters']
        self.allFilenames = data['allFilenames']

    def __repr__(self):
        return "<AllSegments: {0} segments>".format(self.segments_number)

    def getByIndex(self, index):
        """Return a Segment object by a given index number."""

        return self.segments[index]

    def getByComposer(self, composer):
        """Return a new AllSegment object with all Segment objects
        with a given composer as attribute."""

        return _aux_getBy([un for un in self.segments if un.composer == composer], self.save)

    def getByTitle(self, title):
        """Return a new AllSegment object with all Segment objects
        with a given song title as attribute."""

        return _aux_getBy([un for un in self.segments if un.title == title], self.save)

    def getByAmbitus(self, ambitus):
        """Return a new AllSegment object with all Segment objects
        with a given ambitus value as attribute."""

        return _aux_getBy([un for un in self.segments if un.ambitus == ambitus], self.save)

    def getByContourPrime(self, contour_prime):
        """Return a new AllSegment object with all Segment objects
        with a given Contour Prime value as attribute."""

        return _aux_getBy([un for un in self.segments if un.contour_prime == contour_prime], self.save)

    def getByPickup(self, pickup=True):
        """Return a new AllSegment object with all Segment objects
        with pickup measure."""

        return _aux_getBy([un for un in self.segments if un.pickup == pickup], self.save)


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
        return r

    data = {}
    data['allComposers'] = getData(SegmentsList, 'composer')
    data['allTitles'] = getData(SegmentsList, 'title')
    data['allCollections'] = getData(SegmentsList, 'collection')
    data['allContours'] = getData(SegmentsList, 'contour')
    data['allContourSizes'] = getData(SegmentsList, 'contour_size')
    data['allContourPrimes'] = getData(SegmentsList, 'contour_prime')
    data['allAmbitus'] = getData(SegmentsList, 'ambitus')
    data['allTimeSignatures'] = getData(SegmentsList, 'time_signature')
    data['allMeters'] = getData(SegmentsList, 'meter')
    data['allFilenames'] = getData(SegmentsList, 'filename')

    return data

def makeAllSegments(save=False):
    """Return an AllSegment object with all Segment objects saved in a
    pickle or in available collections."""

    SegmentsList = []
    songs = retrieval.load_pickle('songs')
    if save:
        songs = retrieval.load_pickle('songs')
    else:
        songs = song.makeSongCollection(coll, save)
    for s in songs:
        SegmentsList.extend(s.segments)

    d = getSegmentsData(SegmentsList)
    d['segments'] = SegmentsList
    return AllSegments(d, save)
