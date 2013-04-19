#!/usr/bin/env python
# -*- coding: utf-8 -*-

import music21
import _utils
import retrieval
import song


def _aux_getBy(units, save):
    d = getMusicUnitsData(units)
    d['units'] = units
    return AllMusicUnits(d, save)


class AllMusicUnits(object):
    def __init__(self, data, save=False):
        self.save = save
        self.units = data['units']
        self.units_number = len(self.units)

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
        return "<AllMusicUnits: {0} units>".format(self.units_number)

    def getByIndex(self, index):
        return self.units[index]

    def getByComposer(self, composer):
        return _aux_getBy([un for un in self.units if un.composer == composer], self.save)

    def getByTitle(self, title):
        return _aux_getBy([un for un in self.units if un.title == title], self.save)

    def getByAmbitus(self, ambitus):
        return _aux_getBy([un for un in self.units if un.ambitus == ambitus], self.save)

    def getByContourPrime(self, contour_prime):
        return _aux_getBy([un for un in self.units if un.contour_prime == contour_prime], self.save)

    def getByPickup(self, pickup=True):
        return _aux_getBy([un for un in self.units if un.pickup == pickup], self.save)


def getMusicUnitsData(MusicUnitsList):

    def getData(MusicUnitsList, attrib):
        s = set()
        for MusicUnitObj in MusicUnitsList:
            value = getattr(MusicUnitObj, attrib)
            if type(value) == music21.contour.contour.Contour:
                value = tuple(value)
                s.add(value)
                r = [music21.contour.contour.Contour(cseg) for cseg in sorted(s)]
            else:
                s.add(value)
                r = sorted(s)
        return r

    data = {}
    data['allComposers'] = getData(MusicUnitsList, 'composer')
    data['allTitles'] = getData(MusicUnitsList, 'title')
    data['allCollections'] = getData(MusicUnitsList, 'collection')
    data['allContours'] = getData(MusicUnitsList, 'contour')
    data['allContourSizes'] = getData(MusicUnitsList, 'contour_size')
    data['allContourPrimes'] = getData(MusicUnitsList, 'contour_prime')
    data['allAmbitus'] = getData(MusicUnitsList, 'ambitus')
    data['allTimeSignatures'] = getData(MusicUnitsList, 'time_signature')
    data['allMeters'] = getData(MusicUnitsList, 'meter')
    data['allFilenames'] = getData(MusicUnitsList, 'filename')

    return data

def makeAllMusicUnits(save=False):
    MusicUnitsList = []
    songs = retrieval.load_pickle('songs')
    if save:
        songs = retrieval.load_pickle('songs')
    else:
        songs = song.makeSongCollection(coll, save)
    for s in songs:
        MusicUnitsList.extend(s.subUnits)

    d = getMusicUnitsData(MusicUnitsList)
    d['units'] = MusicUnitsList
    return AllMusicUnits(d, save)
