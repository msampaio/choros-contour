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


class Pieces(object):
    """Class for Piece objects filtering."""

    def __init__(self):
        self.objects = None
        self.titles = None
        self.composers = None
        self.cities = None
        self.years = None
        self.size = None

    def __eq__(self, other):
        return _utils.equalityComparisons(self, other)

    def __ne__(self, other):
        return _utils.equalityComparisons(self, other, True)

    def __repr__(self):
        return "<Pieces: {0}>".format(self.size)

    def getByTitle(self, title):
        return makePieces([obj for obj in self.objects if title in obj.title])

    def getByCity(self, city):
        return makePieces([obj for obj in self.objects if city in obj.city])

    def getByYear(self, year):
        if type(year) == int:
            year = str(year)
        return makePieces([obj for obj in self.objects if year in obj.year])

    def getByComposerName(self, composerName):
        def aux(objects, composerName):
            return composerName in ', '.join([o.name for o in objects.composer])
        return makePieces([obj for obj in self.objects if aux(obj, composerName)])

    def getByComposerGender(self, composerGender):
        def aux(objects, composerGender):
            return composerGender in ', '.join([o.gender for o in objects.composer])
        return makePieces([obj for obj in self.objects if aux(obj, composerGender)])

    def getByComposerInstrument(self, composerInstrument):
        def aux(objects, composerInstrument):
            return composerInstrument in ', '.join([o.mainInstrument for o in objects.composer])
        return makePieces([obj for obj in self.objects if aux(obj, composerInstrument)])

    def getByComposerBornYear(self, composerBornYear):
        def aux(objects, composerBornYear):
            if type(composerBornYear) == int:
                composerBornYear = str(composerBornYear)
            return composerBornYear in ', '.join([o.bornYear for o in objects.composer])
        return makePieces([obj for obj in self.objects if aux(obj, composerBornYear)])

    def getByComposerBornCity(self, composerBornCity):
        def aux(objects, composerBornCity):
            return composerBornCity in ', '.join([o.bornCity.name for o in objects.composer if o.bornCity])
        return makePieces([obj for obj in self.objects if aux(obj, composerBornCity)])

    def getByComposerDeathYear(self, composerDeathYear):
        def aux(objects, composerDeathYear):
            if type(composerDeathYear) == int:
                composerDeathYear = str(composerDeathYear)
            return composerDeathYear in ', '.join([o.deathYear for o in objects.composer])
        return makePieces([obj for obj in self.objects if aux(obj, composerDeathYear)])

    def getByComposerDeathCity(self, composerDeathCity):
        def aux(objects, composerDeathCity):
            return composerDeathCity in ', '.join([o.deathCity.name for o in objects.composer if o.deathCity])
        return makePieces([obj for obj in self.objects if aux(obj, composerDeathCity)])


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


def makePieces(piecesObjList):
    """Make a Pieces object from a list of Piece objects."""

    pieces = Pieces()
    pieces.objects = _utils.organizeAndSort(piecesObjList)
    pieces.composers = makeComposers(_utils.flatten([obj.composer for obj in pieces.objects if obj.composer]))
    pieces.titles = _utils.organizeAndSort([obj.title for obj in piecesObjList if obj.title])
    pieces.cities = _utils.organizeAndSort([obj.city for obj in piecesObjList if obj.city])
    pieces.years = _utils.organizeAndSort([obj.year for obj in piecesObjList if obj.year])
    pieces.size = len(pieces.objects)

    return pieces


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
