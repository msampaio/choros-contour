#!/usr/bin/env python
# -*- coding: utf-8 -*-

import music21
import _utils
import data
import song


def _aux_getBy(units, save):
    d = getUnitsData(units)
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

    def __repr__(self):
        return "<AllMusicUnits: {0} units>".format(self.units_number)

    def getByIndex(self, index):
        return self.units[index]

    def getByComposer(self, composer):
        return _aux_getBy([u for u in self.units if u.composer == composer], self.save)

    def getByTitle(self, title):
        return _aux_getBy([u for u in self.units if u.title == title], self.save)

    def getByAmbitus(self, ambitus):
        return _aux_getBy([u for u in self.units if u.ambitus == ambitus], self.save)

    def getByContourPrime(self, contour_prime):
        return _aux_getBy([u for u in self.units if u.contour_prime == contour_prime], self.save)

    def getByPickup(self, pickup=True):
        return _aux_getBy([u for u in self.units if u.pickup == pickup], self.save)


def getUnitsData(units):

    def getData(unit, attrib):
        s = set()
        for unit in units:
            value = getattr(unit, attrib)
            if type(value) == music21.contour.contour.Contour:
                value = tuple(value)
                s.add(value)
                r = [music21.contour.contour.Contour(cseg) for cseg in sorted(s)]
            else:
                s.add(value)
                r = sorted(s)
        return r

    data = {}
    data['allComposers'] = getData(units, 'composer')
    data['allTitles'] = getData(units, 'title')
    data['allCollections'] = getData(units, 'collection')
    data['allContours'] = getData(units, 'contour')
    data['allContourSizes'] = getData(units, 'contour_size')
    data['allContourPrimes'] = getData(units, 'contour_prime')
    data['allAmbitus'] = getData(units, 'ambitus')
    data['allTimeSignatures'] = getData(units, 'time_signature')
    data['allMeters'] = getData(units, 'meter')

    return data

def makeAllMusicUnits(save=False):
    units = []
    for coll in _utils.collections_list('choros-corpus'):
        print "Processing collection {0}...".format(coll)
        try:
            if save:
                songs = data.load_pickle('songs', coll)
            else:
                songs = song.makeSongCollection(coll, save)
            for s in songs:
                units.extend(s.subUnits)
        except:
            print "No .form or .xml phrases in collection {0}".format(coll)

    d = getUnitsData(units)
    d['units'] = units
    return AllMusicUnits(d, save)
