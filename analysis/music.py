#!/usr/bin/env python
# -*- coding: utf-8 -*-

import types
import copy
import itertools
import music21
from music21.contour import Contour
from music21.interval import notesToInterval, notesToChromatic
import _utils


class _FormStructure(object):
    """Class for FormStructure objects."""

    def __init__(self):
        self.formFilename = None
        self.typeOf = None
        self.initial = None
        self.final = None
        self.number = None

    def show(self):
        print "Structure {0}: {1} {2}--{3}".format(self.number, self.typeOf, self.initial, self.final)

    def __repr__(self):
        return "<FormStructure: {0} n.{1}, {2}--{3}>".format(self.typeOf, self.number, self.initial, self.final)


class Form(object):
    """Class for Form objects."""


    def __init__(self):
        self.xmlFilename = None
        self.formFilename = None
        self.sequence = None

    def __repr__(self):
        return "<Form: {0}>".format(self.xmlFilename)

    def show(self):
        """Print the form table such as .form file."""

        for formStructure in self.sequence:
            formStructure.show()

    def getStructure(self, structure, value):
        """Get Structure by a given structure type and its value."""

        return [fs for fs in self.sequence if value == fs.__getattribute__(structure)]


class Note(object):
    """Class for Note objects."""

    def __init__(self):
        self.name = None
        self.code = None
        self.duration = None
        self.octave = None
        self.offset = None

    def __repr__(self):
        return u"<Note: {0}{1}>".format(self.name, self.octave)


class Interval(object):
    """Class for Interval objects."""

    def __init__(self):
        self.value = None
        self.quality = None
        self.direction = None
        self.chromatic = None
        self.diatonic = None
        self.diatonicDirected = None
        self.isConsonant = None
        self.noteStart = None
        self.noteEnd = None

    def __repr__(self):
        return "<Interval: {0}>".format(self.diatonic)


# Class makers
def _makeFormStructure(formFilename, typeOf, initial, final, number):
    formStructure = _FormStructure()
    formStructure.formFilename = formFilename
    formStructure.typeOf = typeOf
    formStructure.initial = initial
    formStructure.final = final
    formStructure.number = number

    return formStructure


def makeForm(xmlFilename):
    """Returns a Form object.

    >>> makeForm('choros-corpus/corpus/TOMP_34E-Minha_vez.xml')
    """

    def makeFormSequence(formFilename):
        """Returns a dictionary with the formal structure of a song
        parsed."""

        def parseFormLine(string, segmentNumber):
            """Cleans string."""

            cleanedStr = _utils.remove_endline(string).strip(' ')
            if cleanedStr not in [' ', '']:
                if list(cleanedStr)[0] != '#':
                    segmentNumber += 1
                    typeOf, i, f = cleanedStr.split()

                    if typeOf == 'p':
                        t = 'Phrase'
                    else:
                        t = 'NonPhrase'

                    formStructure = _makeFormStructure(formFilename, t, int(i), int(f), segmentNumber)

                    return formStructure, segmentNumber

        with open(formFilename, 'r') as f:
            lines = f.readlines()
            segmentNumber = 0
            formSequence = []
            for line in lines:
                result = parseFormLine(line, segmentNumber)
                if result:
                    formSequence.append(result[0])
                    segmentNumber = result[1]
        return formSequence

    form = Form()
    form.xmlFilename = xmlFilename
    form.formFilename = _utils.changeSuffix(xmlFilename, 'form', True)
    form.sequence = makeFormSequence(form.formFilename)

    return form


def makeNote(n):
    """Returns a Note object.

    >>> makeNote(<music21.note.Note>)
    """

    note = Note()
    note.name = n.name
    note.code = music21.musedata.base40.pitchToBase40(n)
    note.duration = n.duration.quarterLength
    note.octave = n.octave
    note.offset = n.offset

    return note


def makeInterval(noteStart, noteEnd):
    """Returns an Interval object.

    >>> makeInterval(<music21.note.Note>, <music21.note.Note)
    """

    interval = Interval()

    interval.noteStart = makeNote(noteStart)
    interval.noteEnd = makeNote(noteEnd)

    music21Interval = notesToInterval(noteStart, noteEnd)

    interval.diatonic = music21Interval.name
    interval.chromatic = music21Interval.chromatic.semitones
    interval.quality = music21Interval.specificName
    interval.value = music21Interval.generic.value
    interval.direction = music21Interval.direction
    interval.isConsonant = music21Interval.isConsonant()

    if interval.direction == 1:
        signal = '+'
    else:
        signal = '-'

    interval.diatonicDirected = '{0}{1}'.format(signal, interval.diatonic)

    return interval


def makeContour(cpointsSeq):
    """Return a Contour object with cpoints, size and prime
    arguments.

    >>> makeContour([1, 5, 3])
    < 1 5 3 >
    """

    cseg = Contour(cpointsSeq)
    cseg.cpoints = tuple(cseg.items)
    cseg.size = len(cseg.cpoints)
    cseg.prime = cseg.reduction_morris()[0]

    # FIXME: Update music21 with contour package to use Sampaio Prime
    # Form Algorithm and remove this action
    i = cseg.inversion()
    r = cseg.retrogression()
    ri = i.retrogression()
    cseg.sampaioPrime = Contour(sorted([list(cseg), list(i), list(r), list(ri)])[0]).translation()

    return cseg


def makeStream(filename):
    """Returns a music21 stream with appended explicit appended notes.

    >>> makeStream('choros-corpus/corpus/TOMP_33E-Lamentos.xml')
    """

    # For some reason Stream([n for n in score.flat.notes]) accumulate
    # notes in the wrong order, so we append them explicitly.

    return music21.converter.parse(filename)


# Other functions
def contourSequenceToTuple(csegsSequence):
    """Return a list of tuples of contour points from a given sequence
    of Contour objects."""

    if len(csegsSequence) > 1:
        if type(data[0]) == Contour:
            csegsSequence = [cseg.cpoints for cseg in csegsSequence]
    return csegsSequence


def scoreEventsEnumerator(score, showNumbers=True):
    """Return a Music21 score stream with all notes and rests numbered
    in order. Each event (note and rest) receives a eventNumber
    attribute."""

    newScore = copy.deepcopy(score)
    part = newScore.getElementsByClass('Part')[0]
    measures = part.getElementsByClass('Measure')
    eventCounter = 0

    for measure in measures:
        events = measure.notesAndRests
        for event in events:
            event.eventNumber = eventCounter
            if showNumbers:
                event.lyric = eventCounter
            eventCounter += 1

    return newScore


def getNotes(score):
    # For some reason Stream([n for n in score.flat.notes]) accumulate
    # notes in the wrong order, so we append them explicitly.

    stream = music21.stream.Stream()
    for n in score.flat.notes.stripTies():
        if n.isChord:
            stream.append(n[-1])
        else:
            stream.append(n)
    return stream


def getIntervals(notes):
    """Return a sequence of Interval objects retrieved from a given
    sequence of music21 Notes objects.
    """

    length = len(notes)
    position = zip(range(length - 1), range(1, length))

    return [makeInterval(notes[x], notes[y]) for x, y in position]


def getDurations(notes):
    """Return a sequence of durations of a given sequence of notes."""

    return [note.duration.quarterLength for note in notes]


def simpleSplitByBeat(notes):
    """Return a given sequence of notes split by beats."""

    seq = [(n.offset, n) for n in notes]
    return [[x[1] for x in list(lst)] for _, lst in itertools.groupby(seq, lambda x: int(x[0]))]


def splitByBeat(score):
    """Return a sequence of notes and rests split by beats from a
    given music21 stream."""

    def noteOrRest(el):
        return type(el) in (music21.note.Note, music21.note.Rest)

    measures = score.getElementsByClass('Measure')
    notes = []

    r = []
    for m in measures:
        g = []
        for el in m:
            if noteOrRest(el):
                g.append(el)
        r.extend(simpleSplitByBeat(g))

    return r


def getBeatPatterns(score):
    """Return the beat patterns of a given sequence of notes in
    quarterLengths."""

    return [tuple([n.duration.quarterLength for n in beat]) for beat in splitByBeat(score)]


def getInfoAboutSource(source):
    """Insert Music information such as Time Signature in Source
    object."""

    print '. Making source {0}'.format(source.idCode.idCode)
    score = source.score
    part = score.getElementsByClass('Part')[0]
    measures = part.getElementsByClass('Measure')
    m1 = measures[0]
    timeSignatureObj = m1.getElementsByClass('TimeSignature')[0]
    source.timeSignature = '/'.join([str(i) for i in timeSignatureObj.numerator, timeSignatureObj.denominator])
    source.meter = timeSignatureObj.beatCountName
    key, source.mode = m1.getElementsByClass('KeySignature')[0].pitchAndMode
    source.key = key.fullName

    return source


def getInfoAboutSegment(segment):
    """Insert Music information such as contour and intervals in
    segment object."""

    score = segment.score
    source = segment.source
    segment.timeSignature = source.timeSignature
    segment.meter = source.meter
    segment.pickup = score.pickup
    segment.measuresNumber = len(score.getElementsByClass(music21.stream.Measure))
    segment.totalLength = sum([n.duration.quarterLength for n in score.flat.notesAndRests])

    notes = getNotes(score)
    _size = len(notes)

    segment.notes = [makeNote(n) for n in notes]
    segment.durations = getDurations(notes)
    segment.beatPatterns = getBeatPatterns(score)
    segment.intervals = getIntervals(notes)
    segment.firstInterval = segment.intervals[0]
    segment.lastInterval = segment.intervals[-1]
    segment.ambitus = score.analyze("ambitus").chromatic.directed

    segment.contour = Contour(score)

    return segment
