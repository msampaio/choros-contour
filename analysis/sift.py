#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import Counter
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

    def getByName(self, composerName, exclusion=False):
        return makeComposers([obj for obj in self.objects if _utils.testIn(composerName, obj.name, exclusion)])

    def getByGender(self, gender, exclusion=False):
        return makeComposers([obj for obj in self.objects if _utils.testIn(gender, obj.gender, exclusion)])

    def getByInstrument(self, instrument, exclusion=False):
        return makeComposers([obj for obj in self.objects if _utils.testIn(instrument, obj.mainInstrument, exclusion)])

    def getByBornCity(self, bornCity, exclusion=False):
        return makeComposers([obj for obj in self.objects if _utils.testIn(bornCity, obj.bornCity, exclusion)])

    def getByBornYear(self, bornYear, exclusion=False):
        if type(bornYear) == int:
            bornYear = str(bornYear)
        return makeComposers([obj for obj in self.objects if _utils.testIn(bornYear, obj.bornYear, exclusion)])

    def getByDeathCity(self, deathCity, exclusion=False):
        return makeComposers([obj for obj in self.objects if _utils.testIn(deathCity, obj.deathCity, exclusion)])

    def getByDeathYear(self, deathYear, exclusion=False):
        if type(deathYear) == int:
            deathYear = str(deathYear)
        return makeComposers([obj for obj in self.objects if _utils.testIn(deathYear, obj.deathYear, exclusion)])


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

    def getByTitle(self, title, exclusion=False):
        return makePieces([obj for obj in self.objects if _utils.testIn(title, obj.title, exclusion)])

    def getByCity(self, city, exclusion=False):
        return makePieces([obj for obj in self.objects if _utils.testIn(city, obj.city, exclusion)])

    def getByYear(self, year, exclusion=False):
        if type(year) == int:
            year = str(year)
        return makePieces([obj for obj in self.objects if _utils.testIn(year, obj.year, exclusion)])

    def getByComposerName(self, composerName, exclusion=False):
        def aux(obj, composerName):
            return _utils.testIn(composerName, ', '.join([o.name for o in obj.composer]), exclusion)
        return makePieces([obj for obj in self.objects if aux(obj, composerName)])

    def getByComposerGender(self, composerGender, exclusion=False):
        def aux(obj, composerGender):
            return _utils.testIn(composerGender, ', '.join([o.gender for o in obj.composer]), exclusion)
        return makePieces([obj for obj in self.objects if aux(obj, composerGender)])

    def getByComposerInstrument(self, composerInstrument, exclusion=False):
        def aux(obj, composerInstrument):
            return _utils.testIn(composerInstrument, ', '.join([o.mainInstrument for o in obj.composer]), exclusion)
        return makePieces([obj for obj in self.objects if aux(obj, composerInstrument)])

    def getByComposerBornYear(self, composerBornYear, exclusion=False):
        def aux(obj, composerBornYear):
            if type(composerBornYear) == int:
                composerBornYear = str(composerBornYear)
            return _utils.testIn(composerBornYear, ', '.join([o.bornYear for o in obj.composer]), exclusion)
        return makePieces([obj for obj in self.objects if aux(obj, composerBornYear)])

    def getByComposerBornCity(self, composerBornCity, exclusion=False):
        def aux(obj, composerBornCity):
            return _utils.testIn(composerBornCity, ', '.join([o.bornCity.name for o in obj.composer if o.bornCity]), exclusion)
        return makePieces([obj for obj in self.objects if aux(obj, composerBornCity)])

    def getByComposerDeathYear(self, composerDeathYear, exclusion=False):
        def aux(obj, composerDeathYear):
            if type(composerDeathYear) == int:
                composerDeathYear = str(composerDeathYear)
            return _utils.testIn(composerDeathYear, ', '.join([o.deathYear for o in obj.composer]), exclusion)
        return makePieces([obj for obj in self.objects if aux(obj, composerDeathYear)])

    def getByComposerDeathCity(self, composerDeathCity, exclusion=False):
        def aux(obj, composerDeathCity):
            return _utils.testIn(composerDeathCity, ', '.join([o.deathCity.name for o in obj.composer if o.deathCity]), exclusion)
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

    def getByComposerName(self, composerName, exclusion=False):
        def aux(obj, composerName):
            return _utils.testIn(composerName, ', '.join([o.name for o in obj.piece.composer]), exclusion)
        return makeSources([obj for obj in self.objects if aux(obj, composerName)])

    def getByComposerGender(self, composerGender, exclusion=False):
        def aux(obj, composerGender):
            return _utils.testIn(composerGender, ', '.join([o.gender for o in obj.piece.composer]), exclusion)
        return makeSources([obj for obj in self.objects if aux(obj, composerGender)])

    def getByComposerInstrument(self, composerInstrument, exclusion=False):
        def aux(obj, composerInstrument):
            return _utils.testIn(composerInstrument, ', '.join([o.mainInstrument for o in obj.piece.composer]), exclusion)
        return makeSources([obj for obj in self.objects if aux(obj, composerInstrument)])

    def getByComposerBornYear(self, composerBornYear, exclusion=False):
        def aux(obj, composerBornYear):
            if type(composerBornYear) == int:
                composerBornYear = str(composerBornYear)
            return _utils.testIn(composerBornYear, ', '.join([o.bornYear for o in obj.piece.composer]), exclusion)
        return makeSources([obj for obj in self.objects if aux(obj, composerBornYear)])

    def getByComposerBornCity(self, composerBornCity, exclusion=False):
        def aux(obj, composerBornCity):
            return _utils.testIn(composerBornCity, ', '.join([o.bornCity.name for o in obj.piece.composer if o.bornCity]), exclusion)
        return makeSources([obj for obj in self.objects if aux(obj, composerBornCity)])

    def getByComposerDeathYear(self, composerDeathYear, exclusion=False):
        def aux(obj, composerDeathYear):
            if type(composerDeathYear) == int:
                composerDeathYear = str(composerDeathYear)
            return _utils.testIn(composerDeathYear, ', '.join([o.deathYear for o in obj.piece.composer]), exclusion)
        return makeSources([obj for obj in self.objects if aux(obj, composerDeathYear)])

    def getByComposerDeathCity(self, composerDeathCity, exclusion=False):
        def aux(obj, composerDeathCity):
            return _utils.testIn(composerDeathCity, ', '.join([o.deathCity.name for o in obj.piece.composer if o.deathCity]), exclusion)
        return makeSources([obj for obj in self.objects if aux(obj, composerDeathCity)])

    def getByPieceTitle(self, title, exclusion=False):
        return makeSources([obj for obj in self.objects if _utils.testIn(title, obj.piece.title, exclusion)])

    def getByPieceCity(self, city, exclusion=False):
        return makeSources([obj for obj in self.objects if _utils.testIn(city, obj.piece.city, exclusion)])

    def getByPieceYear(self, year, exclusion=False):
        if type(year) == int:
            year = str(year)
        return makeSources([obj for obj in self.objects if _utils.testIn(year, obj.piece.year, exclusion)])

    def getByCollectionCode(self, code, volume=None, exclusion=False):
        def aux(obj, code, volume):
            cond1 = code in obj.collection.code
            cond2 = True
            if volume not in (None, u''):
                if type(volume) == int:
                    volume = str(volume)
                cond2 = volume in obj.collection.volume
            return cond1 and cond2

        return makeSources([obj for obj in self.objects if aux(obj, code, volume)])

    def getByIdCode(self, idCode, exclusion=False):
        return makeSources([obj for obj in self.objects if _utils.testIn(idCode, obj.idCode.idCode, exclusion)])

    def getByFilename(self, filename, exclusion=False):
        return makeSources([obj for obj in self.objects if _utils.testIn(filename, obj.filename, exclusion)])


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
        self.durations = None
        self.beatContents = None

    def __eq__(self, other):
        return _utils.equalityComparisons(self, other)

    def __ne__(self, other):
        return _utils.equalityComparisons(self, other, True)

    def __repr__(self):
        return "<Segments: {0}>".format(self.size)

    # getby
    def getByComposerName(self, composerName, exclusion=False):
        def aux(obj, composerName):
            return _utils.testIn(composerName, ', '.join([o.name for o in obj.source.piece.composer]), exclusion)
        return makeSegments([obj for obj in self.objects if aux(obj, composerName)])

    def getByComposerGender(self, composerGender, exclusion=False):
        def aux(obj, composerGender):
            return _utils.testIn(composerGender, ', '.join([o.gender for o in obj.source.piece.composer]), exclusion)
        return makeSegments([obj for obj in self.objects if aux(obj, composerGender)])

    def getByComposerInstrument(self, composerInstrument, exclusion=False):
        def aux(obj, composerInstrument):
            return _utils.testIn(composerInstrument, ', '.join([o.mainInstrument for o in obj.source.piece.composer]), exclusion)
        return makeSegments([obj for obj in self.objects if aux(obj, composerInstrument)])

    def getByComposerBornYear(self, composerBornYear, exclusion=False):
        def aux(obj, composerBornYear):
            if type(composerBornYear) == int:
                composerBornYear = str(composerBornYear)
            return _utils.testIn(composerBornYear, ', '.join([o.bornYear for o in obj.source.piece.composer]), exclusion)
        return makeSegments([obj for obj in self.objects if aux(obj, composerBornYear)])

    def getByComposerBornCity(self, composerBornCity, exclusion=False):
        def aux(obj, composerBornCity):
            return _utils.testIn(composerBornCity, ', '.join([o.bornCity.name for o in obj.source.piece.composer if o.bornCity]), exclusion)
        return makeSegments([obj for obj in self.objects if aux(obj, composerBornCity)])

    def getByComposerDeathYear(self, composerDeathYear, exclusion=False):
        def aux(obj, composerDeathYear):
            if type(composerDeathYear) == int:
                composerDeathYear = str(composerDeathYear)
            return _utils.testIn(composerDeathYear, ', '.join([o.deathYear for o in obj.source.piece.composer]), exclusion)
        return makeSegments([obj for obj in self.objects if aux(obj, composerDeathYear)])

    def getByComposerDeathCity(self, composerDeathCity, exclusion=False):
        def aux(obj, composerDeathCity):
            return _utils.testIn(composerDeathCity, ', '.join([o.deathCity.name for o in obj.source.piece.composer if o.deathCity]), exclusion)
        return makeSegments([obj for obj in self.objects if aux(obj, composerDeathCity)])

    def getByPieceTitle(self, title, exclusion=False):
        return makeSegments([obj for obj in self.objects if _utils.testIn(title, obj.source.piece.title, exclusion)])

    def getByPieceCity(self, city, exclusion=False):
        return makeSegments([obj for obj in self.objects if _utils.testIn(city, obj.source.piece.city, exclusion)])

    def getByPieceYear(self, year, exclusion=False):
        if type(year) == int:
            year = str(year)
        return makeSegments([obj for obj in self.objects if _utils.testIn(year, obj.source.piece.year, exclusion)])

    def getByCollectionCode(self, code, volume=None, exclusion=False):
        def aux(obj, code, volume):
            cond1 = code in obj.source.collection.code
            cond2 = True
            if volume not in (None, u''):
                if type(volume) == int:
                    volume = str(volume)
                cond2 = volume in obj.collection.volume
            return cond1 and cond2

        return makeSegments([obj for obj in self.objects if aux(obj, code, volume)])

    def getByIdCode(self, idCode, exclusion=False):
        return makeSegments([obj for obj in self.objects if _utils.testIn(idCode, obj.source.idCode.idCode, exclusion)])

    def getByFilename(self, filename, exclusion=False):
        return makeSegments([obj for obj in self.objects if _utils.testIn(filename, obj.source.filename, exclusion)])

    def getByTimeSignature(self, timeSignature, exclusion=False):
        return makeSegments([obj for obj in self.objects if _utils.testIn(timeSignature, obj.timeSignature, exclusion)])

    def getByMeter(self, meter, exclusion=False):
        return makeSegments([obj for obj in self.objects if _utils.testIn(meter, obj.meter, exclusion)])

    def getByAmbitus(self, ambitus, higherAmbitus=None, exclusion=False):
        """Returns a Segments object with a given ambitus, or the min
        and max of an ambitus range."""

        if higherAmbitus:
            return makeSegments([obj for obj in self.objects if ambitus <= obj.ambitus <= higherAmbitus])
        else:
            return makeSegments([obj for obj in self.objects if ambitus == obj.ambitus])

    def getByMeasureNumber(self, measuresNumber, higherMeasureNumber=None, exclusion=False):
        """Returns a Segments object with a given number of measures,
        or the min and max of a measures' number range."""

        if higherMeasureNumber:
            return makeSegments([obj for obj in self.objects if measuresNumber <= obj.measuresNumber <= higherMeasureNumber])
        else:
            return makeSegments([obj for obj in self.objects if _utils.testEqual(measuresNumber, obj.measuresNumber, exclusion)])

    def getByContourPrime(self, contourPrime, exclusion=False):
        return makeSegments([obj for obj in self.objects if _utils.testEqual(contourPrime, obj.contourPrime, exclusion)])

    def getByIntervals(self, interval, exclusion=False):
        return makeSegments([obj for obj in self.objects if _utils.testIn(interval, obj.intervals, exclusion)])

    def getByFirstInterval(self, interval, exclusion=False):
        return makeSegments([obj for obj in self.objects if _utils.testEqual(interval, obj.firstInterval, exclusion)])

    def getByLastInterval(self, interval, exclusion=False):
        return makeSegments([obj for obj in self.objects if _utils.testEqual(interval, obj.lastInterval, exclusion)])

    def getByDuration(self, duration, exclusion=False):
        return makeSegments([obj for obj in self.objects if _utils.testIn(duration, obj.durations, exclusion)])

    def getByBeatContents(self, beatContents, exclusion=False):
        return makeSegments([obj for obj in self.objects if _utils.testIn(beatContents, obj.beatContents, exclusion)])

    # count
    def countComposerBornYears(self):
        return Counter(_utils.flatten([[o.bornYear for o in obj.source.piece.composer] for obj in self.objects]))

    def countComposerBornCities(self):
        return Counter(_utils.flatten([[o.bornCity for o in obj.source.piece.composer] for obj in self.objects]))

    def countComposerDeathYears(self):
        return Counter(_utils.flatten([[o.deathYear for o in obj.source.piece.composer] for obj in self.objects]))

    def countComposerDeathCities(self):
        return Counter(_utils.flatten([[o.deathCity for o in obj.source.piece.composer] for obj in self.objects]))

    def countComposerInstruments(self):
        return Counter(_utils.flatten([[o.mainInstrument for o in obj.source.piece.composer] for obj in self.objects]))

    def countContourPrimes(self):
        return contour.counting([obj.contourPrime for obj in self.objects])

    def countIntervals(self):
        return Counter(_utils.flatten([obj.intervals for obj in self.objects]))

    def countFirstIntervals(self):
        return Counter([obj.firstInterval for obj in self.objects])

    def countLastIntervals(self):
        return Counter([obj.lastInterval for obj in self.objects])

    def countMeasuresNumbers(self):
        return Counter([obj.measuresNumber for obj in self.objects])

    def countAmbitus(self):
        return Counter([obj.ambitus for obj in self.objects])

    def countMeter(self):
        return Counter([obj.meter for obj in self.objects])

    def countTimeSignature(self):
        return Counter([obj.timeSignature for obj in self.objects])

    def countDuration(self):
        return Counter(_utils.flatten([obj.durations for obj in self.objects]))

    def countBeatContent(self):
        return Counter(_utils.flatten([obj.beatContents for obj in self.objects]))


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
    segments.firstIntervals = _utils.organizeAndSort([obj.firstInterval for obj in segments.objects if obj.firstInterval])
    segments.lastIntervals = _utils.organizeAndSort([obj.lastInterval for obj in segments.objects if obj.lastInterval])
    segments.durations = _utils.organizeAndSort(_utils.flatten([obj.durations for obj in segments.objects if obj.durations]))
    segments.beatContents = _utils.organizeAndSort(_utils.flatten([obj.beatContents for obj in segments.objects if obj.beatContents]))

    return segments
