#!/usr/bin/env python
# -*- coding: utf-8 -*-

import core
import segment
import _utils
import contour


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


class Segments(object):
    """Class for Segment objects filtering."""

    def __init__(self):
        self.objects = None
        self.composers = None
        self.collections = None
        self.pieces = None
        self.sources = None
        self.size = None
        self.timeSignatures = None
        self.meters = None
        self.ambitus = None
        self.measuresNumbers = None

        self.contourPrimes = None

        self.intervals = None
        self.firstIntervals = None
        self.lastIntervals = None

    def __eq__(self, other):
        return _utils.equalityComparisons(self, other)

    def __ne__(self, other):
        return _utils.equalityComparisons(self, other, True)

    def __repr__(self):
        return "<Segments: {0}>".format(self.size)

    def getByComposerName(self, composerName):
        def aux(obj, composerName):
            return composerName in ', '.join([o.name for o in obj.source.piece.composer])
        return makeSegments([obj for obj in self.objects if aux(obj, composerName)])

    def getByComposerGender(self, composerGender):
        def aux(obj, composerGender):
            return composerGender in ', '.join([o.gender for o in obj.source.piece.composer])
        return makeSegments([obj for obj in self.objects if aux(obj, composerGender)])

    def getByComposerInstrument(self, composerInstrument):
        def aux(obj, composerInstrument):
            return composerInstrument in ', '.join([o.mainInstrument for o in obj.source.piece.composer])
        return makeSegments([obj for obj in self.objects if aux(obj, composerInstrument)])

    def getByComposerBornYear(self, composerBornYear):
        def aux(obj, composerBornYear):
            if type(composerBornYear) == int:
                composerBornYear = str(composerBornYear)
            return composerBornYear in ', '.join([o.bornYear for o in obj.source.piece.composer])
        return makeSegments([obj for obj in self.objects if aux(obj, composerBornYear)])

    def getByComposerBornCity(self, composerBornCity):
        def aux(obj, composerBornCity):
            return composerBornCity in ', '.join([o.bornCity.name for o in obj.source.piece.composer if o.bornCity])
        return makeSegments([obj for obj in self.objects if aux(obj, composerBornCity)])

    def getByComposerDeathYear(self, composerDeathYear):
        def aux(obj, composerDeathYear):
            if type(composerDeathYear) == int:
                composerDeathYear = str(composerDeathYear)
            return composerDeathYear in ', '.join([o.deathYear for o in obj.source.piece.composer])
        return makeSegments([obj for obj in self.objects if aux(obj, composerDeathYear)])

    def getByComposerDeathCity(self, composerDeathCity):
        def aux(obj, composerDeathCity):
            return composerDeathCity in ', '.join([o.deathCity.name for o in obj.source.piece.composer if o.deathCity])
        return makeSegments([obj for obj in self.objects if aux(obj, composerDeathCity)])

    def getByPieceTitle(self, title):
        return makeSegments([obj for obj in self.objects if title in obj.source.piece.title])

    def getByPieceCity(self, city):
        return makeSegments([obj for obj in self.objects if city in obj.source.piece.city])

    def getByPieceYear(self, year):
        if type(year) == int:
            year = str(year)
        return makeSegments([obj for obj in self.objects if year in obj.source.piece.year])

    def getByCollectionCode(self, code, volume=None):
        def aux(obj, code, volume):
            cond1 = code in obj.source.collection.code
            cond2 = True
            if volume not in (None, u''):
                if type(volume) == int:
                    volume = str(volume)
                cond2 = volume in obj.collection.volume
            return cond1 and cond2

        return makeSegments([obj for obj in self.objects if aux(obj, code, volume)])

    def getByIdCode(self, idCode):
        return makeSegments([obj for obj in self.objects if idCode in obj.source.idCode.idCode])

    def getByFilename(self, filename):
        return makeSegments([obj for obj in self.objects if filename in obj.source.filename])

    def getByTimeSignature(self, timeSignature):
        return makeSegments([obj for obj in self.objects if timeSignature in obj.timeSignature])

    def getByMeter(self, meter):
        return makeSegments([obj for obj in self.objects if meter in obj.meter])

    def getByAmbitus(self, ambitus, higherAmbitus=None):
        """Returns a Segments object with a given ambitus, or the min
        and max of an ambitus range."""

        if higherAmbitus:
            return makeSegments([obj for obj in self.objects if ambitus <= obj.ambitus <= higherAmbitus])
        else:
            return makeSegments([obj for obj in self.objects if ambitus == obj.ambitus])

    def getByMeasureNumber(self, measuresNumber, higherMeasureNumber=None):
        """Returns a Segments object with a given number of measures,
        or the min and max of a measures' number range."""

        if higherMeasureNumber:
            return makeSegments([obj for obj in self.objects if measuresNumber <= obj.measuresNumber <= higherMeasureNumber])
        else:
            return makeSegments([obj for obj in self.objects if measuresNumber == obj.measuresNumber])

    def getByContourPrime(self, contourPrime):
        return makeSegments([obj for obj in self.objects if contourPrime == obj.contourPrime])

    def getByIntervals(self, interval):
        return makeSegments([obj for obj in self.objects if interval in obj.intervals])

    def getByFirstInterval(self, interval):
        return makeSegments([obj for obj in self.objects if interval == obj.firstInterval])

    def getByLastInterval(self, interval):
        return makeSegments([obj for obj in self.objects if interval == obj.lastInterval])


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
    sources.composers = makeComposers(_utils.flatten([obj.piece.composer for obj in sources.objects if obj.piece.composer]))
    sources.pieces = makePieces([obj.piece for obj in sources.objects if obj.piece])
    sources.collections = _utils.organizeAndSort([obj.collection for obj in sources.objects if obj.collection])
    sources.idCodes = _utils.organizeAndSort([obj.idCode for obj in sources.objects if obj.idCode])
    sources.filenames = _utils.organizeAndSort([obj.filename for obj in sources.objects if obj.filename])
    sources.size = len(sources.objects)

    return sources


def makeSegments(segmentsObjList):
    """Make a Segments object from a list of Segment objects."""

    segments = Segments()
    segments.objects = _utils.organizeAndSort(segmentsObjList)
    segments.sources = makeSources([obj.source for obj in segments.objects if obj.source])
    segments.pieces = makePieces([obj.source.piece for obj in segments.objects if obj.source.piece])
    segments.composers = makeComposers(_utils.flatten([obj.source.piece.composer for obj in segments.objects if obj.source.piece.composer]))
    segments.collections = _utils.organizeAndSort([obj.source.collection for obj in segments.objects if obj.source.collection])
    segments.size = len(segments.objects)

    segments.timeSignatures = _utils.organizeAndSort([obj.timeSignature for obj in segments.objects if obj.timeSignature])
    segments.meters = _utils.organizeAndSort([obj.meter for obj in segments.objects if obj.meter])
    segments.ambitus = _utils.organizeAndSort([obj.ambitus for obj in segments.objects if obj.ambitus])
    segments.measuresNumbers = _utils.organizeAndSort([obj.measuresNumber for obj in segments.objects if obj.measuresNumber])
    segments.contourPrimes = contour.removeDuplicate([obj.contourPrime for obj in segments.objects if obj.contourPrime])
    segments.intervals = _utils.organizeAndSort(_utils.flatten([obj.intervals for obj in segments.objects if obj.intervals]))
    segments.ambitus = _utils.organizeAndSort([obj.ambitus for obj in segments.objects if obj.ambitus])
    segments.firstIntervals = _utils.organizeAndSort([obj.firstInterval for obj in segments.objects if obj.firstInterval])
    segments.lastIntervals = _utils.organizeAndSort([obj.lastInterval for obj in segments.objects if obj.lastInterval])

    return segments
