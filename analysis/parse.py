#!/usr/bin/env python
# -*- coding: utf-8 -*-

import music21
from music21.contour import Contour
import copy
import _utils
import note
import contour


def sourceParse(filename):
    return music21.converter.parse(filename)


def formParse(filename):
    """Returns a dictionary with the formal structure of a song
    parsed. The argument is the name of xml file, but the function
    parses the .form file in the same directory of the xml one."""

    formName = _utils.changeSuffix(filename, 'form', True)

    with open(formName, 'r') as f:
        lines = f.readlines()
        seq = []
        for el in lines:
            seq_el = _utils.remove_endline(el).strip(' ')
            if seq_el not in [' ', '']:
                seq.append(seq_el)
    form = []
    segment_number = 0

    for el in seq:
        if list(el)[0] != '#':
            typeof, i, f = el.split()
            initial = int(i)
            final = int(f)
            segment_number += 1

            segment_form = {}
            segment_form['initial'] = initial
            segment_form['final'] = final
            segment_form['number'] = segment_number

            if typeof == 'p':
                segment_form['typeof'] = 'Phrase'
            else:
                segment_form['typeof'] = 'NonPhrase'
            form.append(segment_form)

    return form


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


def getInfoAboutSource(sourceObj):
    """Insert Music information such as Time Signature in Source
    object."""

    score = sourceObj.score
    part = score.getElementsByClass('Part')[0]
    measures = part.getElementsByClass('Measure')
    m1 = measures[0]
    timeSignatureObj = m1.getElementsByClass('TimeSignature')[0]
    sourceObj.timeSignature = '/'.join([str(i) for i in timeSignatureObj.numerator, timeSignatureObj.denominator])
    sourceObj.meter = timeSignatureObj.beatCountName
    sourceObj.key, sourceObj.mode = m1.getElementsByClass('KeySignature')[0].pitchAndMode

    return sourceObj


def getInfoAboutSegment(segmentObj):
    """Insert Music information such as contour and intervals in
    segment object."""

    score = segmentObj.score
    sourceObj = segmentObj.source
    segmentObj.timeSignature = sourceObj.timeSignature
    segmentObj.meter = sourceObj.meter
    segmentObj.pickup = score.pickup
    segmentObj.measuresNumber = len(score.getElementsByClass(music21.stream.Measure))
    segmentObj.totalLength = sum([n.duration.quarterLength for n in score.flat.notesAndRests])

    notes = note.songNotes(score)
    _size = len(notes)

    segmentObj.notes = [note.makeNote(n) for n in notes]
    segmentObj.durations = note.durations(notes)
    segmentObj.beatContents = note.beatContents(score)
    segmentObj.intervals = note.intervalsWithoutDirection(notes)
    segmentObj.intervalsWithDirection = note.intervalsWithDirection(notes)
    segmentObj.firstInterval = note.notesToChromatic(notes[0], notes[1]).directed
    segmentObj.lastInterval = note.notesToChromatic(notes[_size - 2], notes[_size - 1]).directed
    segmentObj.ambitus = score.analyze("ambitus").chromatic.directed

    segmentObj.contour = Contour(score)
    segmentObj.contourSize = len(segmentObj.contour)
    segmentObj.contourPrime = contour.sampaio(segmentObj.contour.reduction_morris()[0])

    return segmentObj
