#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import os
import music21
import _utils
import idcode
import music


# classes
class Structure(object):
    """Class for Structure objects. It's a super class for the classes
    Composer, Collection, Piece, Source and Segment."""

    def __init__(self):
        self.type = None

    def getAttrib(self, attribString):
        """Return the object's attribute from the attribstring.

        >>> Source().getAttrib('piece.composers')
        """

        obj = copy.deepcopy(self)
        args = attribString.split('.')
        for arg in args:
            if type(obj) == list and structureTypeCheck(obj[0]):
                obj = [singleObj.getAttrib(arg) for singleObj in obj]
                if len(obj) == 1:
                    obj = obj[0]
            else:
                obj = copy.deepcopy(obj.__getattribute__(arg))
        return obj


class Composer(Structure):
    """Class for Composer objects."""

    def __init__(self):
        self.name = None
        self.gender = None
        self.bornYear = None
        self.deathYear = None
        self.instrument = None

    def __eq__(self, other):
        return _utils.equalityComparisons(self, other)

    def __ne__(self, other):
        return _utils.equalityComparisons(self, other, True)

    def __repr__(self):
        return "<Composer: {0}, {1}--{2}>".format(self.name, self.bornYear, self.deathYear)

    def lifeTime(self):
        """Returns the composer's lifetime."""

        if self.deathYear and self.bornYear:
            return self.deathYear - self.bornYear


class Piece(Structure):
    """Class for Piece objects."""

    def __init__(self):
        self.title = None
        self.composers = None # a sequence of Composer objects
        self.city = None
        self.year = None

    def __eq__(self, other):
        return _utils.equalityComparisons(self, other)

    def __ne__(self, other):
        return _utils.equalityComparisons(self, other, True)

    def __repr__(self):
        return "<Piece: {0} ({1})>".format(self.title, self.makeComposersString())

    def makeComposersString(self):
        if len(self.composers) > 1:
            return ', '.join([composer.name for composer in self.composers])
        else:
            return self.composers[0].name


class Collection(Structure):
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


class Source(Structure):
    """Class for Source objects."""

    def __init__(self):
        self.piece = None # a Piece object
        self.collection = None # a Collection object
        self.idCode = None # an idcode.IdCode object
        self.filename = None
        self.form = None # a music.Form object
        self.score = None # a music21.stream object

        self.timeSignature = None
        self.meter = None
        self.key = None
        self.mode = None

    def __eq__(self, other):
        return _utils.equalityComparisons(self, other)

    def __ne__(self, other):
        return _utils.equalityComparisons(self, other, True)

    def __repr__(self):
        if self.idCode:
            idCode = self.idCode.idCode
        else:
            idCode = None
        return "<Source: {0}, {1}>".format(self.piece.title, idCode)

    def makeScore(self):
        """Create a Music21 stream object in score attribute and get
        all info about the source."""

        if self.filename:
            if not self.score:
                self.score = music.makeStream(self.filename)
                self = music.getInfoAboutSource(self)
            if not self.form and os.path.exists(_utils.changeSuffix(self.filename, 'form', True)):
                self.form = music.makeForm(self.filename)


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

        def makeNewScore(measures, params, keepList, measureNumberCounter, newMeasureNumberCounter):
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


class Segment(Structure):
    """Class for segment objects."""

    def __init__(self):

        self.source = None # a Source object

        self.score = None # a music21.stream object
        self.timeSignature = None
        self.meter = None
        self.ambitus = None
        self.pickup = None
        self.measuresNumber = None
        self.totalLength = None

        self.contour = None # a music.Contour object

        self.notes = None # a music.Note object
        self.intervals = None # a sequence of music.Interval objects
        self.intervalsWithDirection = None
        self.firstInterval = None # a music.Interval object
        self.lastInterval = None # a music.Interval object

        self.durations = None # an array of float numbers
        self.beatPatterns = None # an array

        self.typeOf = None # a string
        self.orderNumber = None # an integer

        self.initialEvent = None # an integer
        self.finalEvent = None # an integer

    def __repr__(self):
        title = self.source.piece.title
        composers = self.source.piece.makeComposersString()
        return "<Segment {0}: {1} ({2})>".format(self.orderNumber, title, composers)


# functions
def makeComposer(name, bornYear=None, deathYear=None, gender='M', instrument=None):
    """Return a Composer object with the given attributes. The year
    must be an integer."""

    composer = Composer()
    composer.name = name
    composer.gender = gender
    composer.instrument = instrument
    composer.bornYear = bornYear
    composer.deathYear = deathYear

    return composer


def makePiece(title, composers, year=None, city=None):
    """Return a Piece object with the given attributes. The composer
    attribute must be a sequence of Composer objects, and the year
    must be an integer such as 1977.

    >>> makePiece('Lamentos', [<Composer: Pixinguinha, 1897--1973>], 1928, 'Rio de Janeiro')
    """

    piece = Piece()

    piece.title = title
    piece.year = year
    piece.composers = composers
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


def makeSource(piece, collection, filename=None, score=False):
    """Return a Source object with the given attributes. The arguments
    piece and collection must be Piece and Collection objects,
    respectively. The score argument define if a score argument will
    be return.

    >>> makeSource(<Piece: Lamentos, Pixinguinha>, <Collection: O melhor de Pixinguinha>, 'TOMP_33E-Lamentos.xml')
    """

    source = Source()

    source.piece = piece
    source.collection = collection
    if filename :
        source.filename = filename
        source.idCode = idcode.getIdCodeByFilename(filename)
        if os.path.exists(_utils.changeSuffix(filename, 'form', True)):
            source.form = music.makeForm(filename)
        if score:
            source.makeScore()
        else:
            source.score = None
    #     if score:
    #         source.score = music.makeStream(filename)
    #         source = music.getInfoAboutSource(source)
    #     if os.path.exists(_utils.changeSuffix(filename, 'form', True)):
    #         source.form = music.makeForm(filename)

    return source


def makeSegment(source, formStructure, savePickle):
    """Return a Segment object from given Source object, formStructure object,
    and an order number."""

    print '.. Making segment {0}'.format(formStructure.number)
    segment = Segment()

    segment.typeOf = formStructure.typeOf
    segment.orderNumber = formStructure.number
    segment.initialEvent = formStructure.initial
    segment.finalEvent = formStructure.final

    segment.source = source
    segment.score = segment.source.getExcerpt(segment.initialEvent, segment.finalEvent)
    segment = music.getInfoAboutSegment(segment)
    if savePickle:
        segment.score = None

    return segment


def makeSegments(source, savePickle=False):
    """Return a segment object from a given Source Object."""

    if not source.score:
        source.makeScore()

    source = music.getInfoAboutSource(source)
    if source.form:
        segments = [makeSegment(source, formStructure, savePickle) for formStructure in source.form.sequence]
    else:
        segments = None
    if savePickle:
        source.score = None
    return segments


def structureTypeCheck(obj):
    """Returns True if the given object is a musical structure."""

    objectType = obj.__class__.__name__
    classes = ['Segment', 'Source', 'Collection', 'Piece', 'Composer']
    return objectType in classes
