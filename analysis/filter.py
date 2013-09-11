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
        def aux(obj, composerName):
            return composerName in ', '.join([o.name for o in obj.composer])
        return makePieces([obj for obj in self.objects if aux(obj, composerName)])

    def getByComposerGender(self, composerGender):
        def aux(obj, composerGender):
            return composerGender in ', '.join([o.gender for o in obj.composer])
        return makePieces([obj for obj in self.objects if aux(obj, composerGender)])

    def getByComposerInstrument(self, composerInstrument):
        def aux(obj, composerInstrument):
            return composerInstrument in ', '.join([o.mainInstrument for o in obj.composer])
        return makePieces([obj for obj in self.objects if aux(obj, composerInstrument)])

    def getByComposerBornYear(self, composerBornYear):
        def aux(obj, composerBornYear):
            if type(composerBornYear) == int:
                composerBornYear = str(composerBornYear)
            return composerBornYear in ', '.join([o.bornYear for o in obj.composer])
        return makePieces([obj for obj in self.objects if aux(obj, composerBornYear)])

    def getByComposerBornCity(self, composerBornCity):
        def aux(obj, composerBornCity):
            return composerBornCity in ', '.join([o.bornCity.name for o in obj.composer if o.bornCity])
        return makePieces([obj for obj in self.objects if aux(obj, composerBornCity)])

    def getByComposerDeathYear(self, composerDeathYear):
        def aux(obj, composerDeathYear):
            if type(composerDeathYear) == int:
                composerDeathYear = str(composerDeathYear)
            return composerDeathYear in ', '.join([o.deathYear for o in obj.composer])
        return makePieces([obj for obj in self.objects if aux(obj, composerDeathYear)])

    def getByComposerDeathCity(self, composerDeathCity):
        def aux(obj, composerDeathCity):
            return composerDeathCity in ', '.join([o.deathCity.name for o in obj.composer if o.deathCity])
        return makePieces([obj for obj in self.objects if aux(obj, composerDeathCity)])


class Sources(object):
    """Class for Source objects filtering."""

    def __init__(self):
        self.objects = None
        self.composers = None
        self.pieces = None
        self.collections = None
        self.idCodes = None
        self.filenames = None
        self.size = None

    def __eq__(self, other):
        return _utils.equalityComparisons(self, other)

    def __ne__(self, other):
        return _utils.equalityComparisons(self, other, True)

    def __repr__(self):
        return "<Sources: {0}>".format(self.size)

    def getByComposerName(self, composerName):
        def aux(obj, composerName):
            return composerName in ', '.join([o.name for o in obj.piece.composer])
        return makeSources([obj for obj in self.objects if aux(obj, composerName)])

    def getByComposerGender(self, composerGender):
        def aux(obj, composerGender):
            return composerGender in ', '.join([o.gender for o in obj.piece.composer])
        return makeSources([obj for obj in self.objects if aux(obj, composerGender)])

    def getByComposerInstrument(self, composerInstrument):
        def aux(obj, composerInstrument):
            return composerInstrument in ', '.join([o.mainInstrument for o in obj.piece.composer])
        return makeSources([obj for obj in self.objects if aux(obj, composerInstrument)])

    def getByComposerBornYear(self, composerBornYear):
        def aux(obj, composerBornYear):
            if type(composerBornYear) == int:
                composerBornYear = str(composerBornYear)
            return composerBornYear in ', '.join([o.bornYear for o in obj.piece.composer])
        return makeSources([obj for obj in self.objects if aux(obj, composerBornYear)])

    def getByComposerBornCity(self, composerBornCity):
        def aux(obj, composerBornCity):
            return composerBornCity in ', '.join([o.bornCity.name for o in obj.piece.composer if o.bornCity])
        return makeSources([obj for obj in self.objects if aux(obj, composerBornCity)])

    def getByComposerDeathYear(self, composerDeathYear):
        def aux(obj, composerDeathYear):
            if type(composerDeathYear) == int:
                composerDeathYear = str(composerDeathYear)
            return composerDeathYear in ', '.join([o.deathYear for o in obj.piece.composer])
        return makeSources([obj for obj in self.objects if aux(obj, composerDeathYear)])

    def getByComposerDeathCity(self, composerDeathCity):
        def aux(obj, composerDeathCity):
            return composerDeathCity in ', '.join([o.deathCity.name for o in obj.piece.composer if o.deathCity])
        return makeSources([obj for obj in self.objects if aux(obj, composerDeathCity)])

    def getByPieceTitle(self, title):
        return makeSources([obj for obj in self.objects if title in obj.piece.title])

    def getByPieceCity(self, city):
        return makeSources([obj for obj in self.objects if city in obj.piece.city])

    def getByPieceYear(self, year):
        if type(year) == int:
            year = str(year)
        return makeSources([obj for obj in self.objects if year in obj.piece.year])

    def getByCollectionCode(self, code, volume=None):
        def aux(obj, code, volume):
            cond1 = code in obj.collection.code
            cond2 = True
            if volume not in (None, u''):
                if type(volume) == int:
                    volume = str(volume)
                cond2 = volume in obj.collection.volume
            return cond1 and cond2

        return makeSources([obj for obj in self.objects if aux(obj, code, volume)])

    def getByIdCode(self, idCode):
        return makeSources([obj for obj in self.objects if idCode in obj.idCode.idCode])

    def getByFilename(self, filename):
        return makeSources([obj for obj in self.objects if filename in obj.filename])


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


def makeSources(sourcesObjList):
    """Make a Sources object from a list of Source objects."""

    sources = Sources()
    sources.objects = _utils.organizeAndSort(sourcesObjList)
    sources.pieces = makePieces([obj.piece for obj in sources.objects if obj.piece])
    sources.collections = _utils.organizeAndSort([obj.collection for obj in sources.objects if obj.collection])
    sources.idCodes = _utils.organizeAndSort([obj.idCode for obj in sources.objects if obj.idCode])
    sources.filenames = _utils.organizeAndSort([obj.filename for obj in sources.objects if obj.filename])
    sources.size = len(sources.objects)

    return sources
