#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import copy
import music21
import _utils
import idcode
import parse


class City(object):
    """Class for City objects."""

    def __init__(self):

        self.name = None
        self.province = None

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def __eq__(self, other):
        return _utils.equalityComparisons(self, other)

    def __ne__(self, other):
        return _utils.equalityComparisons(self, other, True)

    def __repr__(self):
        return "<City: {0}, {1}>".format(self.name, self.province)


class Composer(object):
    """Class for Composer objects."""
    
    def __init__(self):

        self.name = None
        self.gender = None
        self.bornCity = None
        self.bornYear = None
        self.deathCity = None
        self.deathYear = None
        self.mainInstrument = None

    def __eq__(self, other):
        return _utils.equalityComparisons(self, other)

    def __ne__(self, other):
        return _utils.equalityComparisons(self, other, True)

    def __repr__(self):
        if self.bornCity:
            bornCity = self.bornCity.province
        else:
            bornCity = None

        return "<Composer: {0}, {1}, {2}--{3}>".format(self.name, bornCity, self.bornYear, self.deathYear)


class Piece(object):
    """Class for Piece objects."""

    def __init__(self):

        self.title = None
        self.composer = None
        self.city = None
        self.year = None

    def __eq__(self, other):
        return _utils.equalityComparisons(self, other)

    def __ne__(self, other):
        return _utils.equalityComparisons(self, other, True)

    def __repr__(self):
        return "<Piece: {0} ({1})>".format(self.title, self.makeComposersString())

    def makeComposersString(self):
        return ', '.join([composer.name for composer in self.composer])


class Collection(object):
    """Class for Collection objects."""

    def __init__(self):

        self.title = None
        self.author = None
        self.publisher = None
        self.volume = None
        self.code = None

    def __eq__(self, other):
        return _utils.equalityComparisons(self, other)

    def __ne__(self, other):
        return _utils.equalityComparisons(self, other, True)

    def __repr__(self):
        return "<Collection: {0}, vol.{1}>".format(self.title, self.volume)

    def makeCollectionCode(self):
        """Return a string with the collection code."""

        initials = [word[0] for word in self.title.split(' ') if word[0].isupper()]
        self.code = ''.join(initials)
    

class Source(object):
    """Class for Source objects."""

    def __init__(self):

        self.piece = None
        self.collection = None
        self.idCode = None
        self.filename = None
        self.formSeq = None
        self.score = None

    def __eq__(self, other):
        return _utils.equalityComparisons(self, other)

    def __ne__(self, other):
        return _utils.equalityComparisons(self, other, True)

    def __repr__(self):
        return "<Source: {0}, {1}>".format(self.piece.title, self.idCode.idCode)

    def makeScore(self):
        """Create a Music21 stream object in score attribute."""

        if not self.score:
            self.score = parse.sourceParse(self.filename)

    def getExcerpt(self, initial, final, showNumbers=False):
        """Return a score (music21.stream.Stream) object with a
        portion of the Song. The portion includes all numbered music
        events between initial and final values."""

        def getParameters(measures):
            """Return a dictionary with clef, key and time parameters of
            the given measures."""

            m1 = measures[0]
            # song data
            params = {}
            params['clef'] = m1.getElementsByClass('Clef')[0]
            params['key_signature'] = m1.getElementsByClass('KeySignature')[0]
            params['time_signature'] = m1.getElementsByClass('TimeSignature')[0]
            return params

        def makeMeasure(measure, params, keepList, firstMeasureTest):
            """Returns a music21.stream.Measure object from a given
            measure and list of numbers of the events that will be
            kept in the new object."""

            events = [event for event in measure.notesAndRests if event.eventNumber in keepList]
            newMeasure = music21.stream.Measure()

            # padding value for small length measures. Pickup measures or not
            eventsLength = sum((event.quarterLength for event in events))
            measureLength = params['time_signature'].totalLength
            pad = measureLength - eventsLength

            # tests if measure has pickup
            if measure.notesAndRests[0] != events[0]:
                newMeasure.pickup = True
                if pad != 0:
                    newMeasure.paddingLeft = pad
            else:
                newMeasure.pickup = None

            # insert params only in segment's first measure
            if firstMeasureTest:
                for values in params.values():
                    newMeasure.append(values)

            for event in events:
                newMeasure.append(event)

            # complete last measure with pad
            if pad != 0 and not newMeasure.pickup:
                newMeasure.paddingRight = pad

            return newMeasure

        def enumerateEvents(part):
            """Save 'eventNumber' and 'lyric' in note/rest events, and
            'events' with event numbers in measures."""

            eventCounter = 0
            for measure in part:
                if type(measure) == music21.stream.Measure:
                    measureEventNumbers = []
                    for event in measure:
                        if type(event) in (music21.note.Note, music21.note.Rest):
                            eventCounter += 1
                            event.eventNumber = eventCounter
                            # show enumeration as lyrics
                            if showNumbers:
                                event.lyric = eventCounter
                            measureEventNumbers.append(eventCounter)
                    measure.events = measureEventNumbers

        def makeNewScore(measures, params, keepList, measureNumber, newMeasureNumberCounter):
            """Make a new score with events given in keepList. Return
            counters."""

            for measure in measures:
                if any([(ev in keepList) for ev in measure.events]):
                    newMeasureNumberCounter += 1
                    if newMeasureNumberCounter == 1:
                        firstMeasureTest = True
                    else:
                        firstMeasureTest = False
                    newMeasure = makeMeasure(measure, params, keepList, firstMeasureTest)
                    if newMeasure.pickup:
                        newScore.pickup = True
                        newMeasure.pickup = None
                        newMeasure.number = 0
                        measureNumberCounter = 0
                    else:
                        newMeasure.number = measureNumberCounter
                    measureNumberCounter += 1
                    newScore.append(newMeasure)
            return measureNumberCounter, newMeasureNumberCounter

        keepList = range(initial, final + 1)

        part = copy.deepcopy(self.score).getElementsByClass('Part')[0]
        measures = part.getElementsByClass('Measure')
        params = getParameters(measures)

        # create score
        newScore = music21.stream.Stream()
        newScore.initial = initial
        newScore.final = final
        newScore.pickup = False

        # FIXME: retrieve from musicological file
        # newScore.metadata.title = self.title
        # newScore.metadata.composer = self.composersString
        # newScore.insert(music21.metadata.Metadata())

        measureNumberCounter = 1
        newMeasureNumberCounter = 0

        enumerateEvents(part)
        measureNumberCounter, newMeasureNumberCounter = makeNewScore(measures, params, keepList, measureNumberCounter, newMeasureNumberCounter)

        return newScore

    def xmlWrite(self, path=None, suffix='numbered'):
        """Save a score object in a xml file."""

        if not self.score:
            self.makeScore()
        dirname = os.path.dirname(self.filename)
        basename = os.path.basename(self.filename).split('.')[0] + ' - {0}.xml'.format(suffix)
        if path:
            dirname = path
        dest = os.path.join(dirname, basename)
        print "Writing xml file in {0}".format(dest)
        parse.scoreEventsEnumerator(self.score).write('musicxml', dest)

def makeCity(name, province):
    """Return a City object with the given attributes."""

    city = City()
    city.name = name
    city.province = province

    return city


def makeComposer(name, gender='M', bornCityObj=None, bornYear=None, deathCityObj=None, deathYear=None, mainInstrument=None):
    """Return a Composer object with the given attributes. The year
    must be an integer."""

    composer = Composer()
    composer.name = name
    composer.gender = gender
    composer.bornCity = bornCityObj
    composer.deathCity = deathCityObj
    composer.mainInstrument = mainInstrument
    composer.bornYear = bornYear
    composer.deathYear = deathYear

    return composer


def makePiece(title, composer, year=None, subtitle=None, city=None):
    """Return a Piece object with the given attributes. The year must
    be an integer such as 1977."""

    piece = Piece()

    piece.title = title
    piece.year = year
    piece.subtitle = subtitle
    piece.composer = composer
    piece.city = city

    return piece


def makeCollection(title, authorList, publisher, volume=None):
    """Return a Collection object with the given attributes."""

    collection = Collection()
    
    collection.title = title
    collection.author = authorList
    collection.publisher = publisher
    collection.volume = volume
    collection.makeCollectionCode()

    return collection


def makeSource(pieceObj, collectionObj, filename=None):
    """Return a Source object with the given attributes."""

    source = Source()

    source.piece = pieceObj
    source.collection = collectionObj
    if filename:
        source.filename = filename
        source.idCode = idcode.getIdCodeByFilename(filename)
        source.score = parse.sourceParse(filename)
        source.formSeq = parse.formParse(filename)

    return source
