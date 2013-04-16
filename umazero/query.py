#!/usr/bin/env python
# -*- coding: utf-8 -*-

import phrase
import _utils
import data


class AllMusicUnits(object):
    def __init__(self, units, save=False):
        self.save = save
        self.units = units
        self.units_number = len(units)



    def __repr__(self):
        return "<AllMusicUnits: {0} units>".format(self.units_number)

    def getByIndex(self, index):
        return self.units[index]

    def getByComposer(self, composer):
        result = [u for u in self.units if u.composer == composer]
        return AllMusicUnits([el for el in result if el], self.save)

    def getByTitle(self, title):
        result = [u for u in self.units if u.title == title]
        return AllMusicUnits([el for el in result if el], self.save)

    def getByAmbitus(self, ambitus):
        result = [u for u in self.units if u.ambitus == ambitus]
        return AllMusicUnits([el for el in result if el], self.save)

    def getByContourPrime(self, contourprime):
        result = [u for u in self.units if u.contour_prime == contourprime]
        return AllMusicUnits([el for el in result if el], self.save)

    def getByPickup(self, pickup=True):
        result = [u for u in self.units if u.pickup == pickup]
        return AllMusicUnits([el for el in result if el], self.save)


def getUnitsData(units):

    def getData(unit, attrib):
        s = set()
        for unit in units:
            s.add(getattr(unit, attrib))
        return sorted(s)

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
                songs = song.makeSongCollection(coll, save)
            else:
                songs = data.load_pickle(coll)
            units.extend([s.subUnits for s in songs])
        except:
            print "No .phrase or .xml phrases in collection {0}".format(coll)
    return AllMusicUnits(units[0], save)
