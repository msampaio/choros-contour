#!/usr/bin/env python
# -*- coding: utf-8 -*-

import core
import segment
import _utils


class FilterError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


class Composers(object):
    """Class for Composer objects filtering."""

    def __init__(self):
        self.objects = None
        self.composers = None
        self.bornCities = None
        self.bornYears = None
        self.deathCities = None
        self.deathYears = None
        self.mainInstruments = None
        self.size = None

    def __eq__(self, other):
        return _utils.equalityComparisons(self, other)

    def __ne__(self, other):
        return _utils.equalityComparisons(self, other, True)

    def __repr__(self):
        return "<Composers: {0}>".format(self.size)

    def getByName(self, composerName):
        return makeComposers([obj for obj in self.objects if composerName in obj.name])

    def getByGender(self, gender):
        return makeComposers([obj for obj in self.objects if gender in obj.gender])

    def getByInstrument(self, instrument):
        return makeComposers([obj for obj in self.objects if instrument in obj.mainInstrument])

    def getByBornCity(self, bornCity):
        return makeComposers([obj for obj in self.objects if bornCity in obj.bornCity])

    def getByBornYear(self, bornYear):
        if type(bornYear) == int:
            bornYear = str(bornYear)
        return makeComposers([obj for obj in self.objects if bornYear in obj.bornYear])

    def getByDeathCity(self, deathCity):
        return makeComposers([obj for obj in self.objects if deathCity in obj.deathCity])

    def getByDeathYear(self, deathYear):
        if type(deathYear) == int:
            deathYear = str(deathYear)
        return makeComposers([obj for obj in self.objects if deathYear in obj.deathYear])


def makeComposers(composersObjList):
    """Make a Composers object from a list of Composer objects."""

    composers = Composers()
    composers.objects = _utils.organizeAndSort(composersObjList)
    composers.composers = _utils.organizeAndSort([obj.name for obj in composers.objects if obj.name])
    composers.bornCities = _utils.organizeAndSort([obj.bornCity for obj in composers.objects if obj.bornCity])
    composers.bornYears = _utils.organizeAndSort([obj.bornYear for obj in composers.objects if obj.bornYear])
    composers.deathCities = _utils.organizeAndSort([obj.deathCity for obj in composers.objects if obj.deathCity])
    composers.deathYears = _utils.organizeAndSort([obj.deathYear for obj in composers.objects if obj.deathYear])
    composers.size = len(composers.objects)

    return composers

def getByComposer(objList, composerName):
    """Return a filtered list of objects by a given composer name."""

    def aux(composerName, composerList):
        return any([composerName in obj.name for obj in composerList])

    obj1 = objList[0]
    if type(obj1) == core.Piece:
        return [obj for obj in objList if aux(composerName, obj.composer)]
    elif type(obj1) == core.Source:
        return [obj for obj in objList if aux(composerName, obj.piece.composer)]
    elif type(obj1) == segment.Segment:
        return [obj for obj in objList if aux(composerName, obj.source.piece.composer)]
    else:
        print type(obj1)
        raise FilterError('Wrong object list. Try Piece, Source or Segment')


def getByIdCode(objList, idCodeStr):
    """Return a filtered list of objects by a given composer name."""

    def aux(idCodeStr, obj):
        objIdCode = obj.idCode.idCode

        return objIdCode  == idCodeStr or objIdCode.split('-')[0] == idCodeStr.split('-')[0]

    obj1 = objList[0]
    if type(obj1) == core.Source:
        return [obj for obj in objList if aux(idCodeStr, obj)]
    elif type(obj1) == segment.Segment:
        return [obj for obj in objList if aux(idCodeStr, obj.source)]
    else:
        raise FilterError('Wrong object list. Try Source or Segment')


def getByPieceTitle(objList, pieceTitle):
    """Return a filtered list of objects by a given composer name."""

    def aux(pieceTitle, obj):
        objPieceTitle = obj.title

        return objPieceTitle == pieceTitle or pieceTitle in objPieceTitle

    obj1 = objList[0]
    if type(obj1) == core.Piece:
        return [obj for obj in objList if aux(pieceTitle, obj)]
    elif type(obj1) == core.Source:
        return [obj for obj in objList if aux(pieceTitle, obj.piece)]
    elif type(obj1) == segment.Segment:
        return [obj for obj in objList if aux(pieceTitle, obj.source.piece)]
    else:
        raise FilterError('Wrong object list. Try Piece, Source or Segment')


def getByComposerInstrument(objList, composerInstrument):
    """Return a filtered list of objects by a given composer name."""

    def aux(composerInstrument, composerList):
        return any([composerInstrument in obj.mainInstrument for obj in composerList])

    obj1 = objList[0]
    if type(obj1) == core.Piece:
        return [obj for obj in objList if aux(composerInstrument, obj.composer)]
    elif type(obj1) == core.Source:
        return [obj for obj in objList if aux(composerInstrument, obj.piece.composer)]
    elif type(obj1) == segment.Segment:
        return [obj for obj in objList if aux(composerInstrument, obj.source.piece.composer)]
    else:
        raise FilterError('Wrong object list. Try Piece, Source or Segment')
