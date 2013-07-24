#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import Counter
import _utils
import intervals
import contour
import duration


def allIntervals(allSegmentsObj, composer, percentage=True):
    """Return a Counter dictionary with percentage values of all
    intervals classification of a given composer.

    >>> allIntervals(allseg, 'Waldyr Azevedo')
    {'m10': 1.2170889220069547, 'M7': 0.07451564828614009, ... , 'M10': 0.024838549428713365, 'AA1': 0.09935419771485346}
    """

    composerSegments = allSegmentsObj.getByComposer(composer).segments
    counterObj = Counter()

    for seg in composerSegments:
        myData = seg.intervals
        counterObj = counterObj + Counter(myData)

    if percentage:
        counterObj = _utils.percentage(counterObj)

    return counterObj


def stepLeapArpeggio(allSegmentsObj, composer, percentage=True):
    """Return a Counter dictionary with percentage values of all
    steps, leaps and arpeggios classification of a given composer.

    >>> stepLeapArpeggio(allseg, 'Waldyr Azevedo')
    {'Leap': 21.609538002980624, 'Repetition': 8.917039244908098, 'Step': 47.66517635370094, '3rd': 21.808246398410333}
    """

    composerSegments = allSegmentsObj.getByComposer(composer).segments
    counterObj = Counter()

    for seg in composerSegments:
        myData = intervals.step_leap_arpeggio(seg.intervals)
        counterObj = counterObj + Counter(myData)

    if percentage:
        counterObj = _utils.percentage(counterObj)

    return counterObj


def consonance(allSegmentsObj, composer, percentage=True):
    """Return a Counter dictionary with percentage values consonance
    intervals classification of a given composer.

    >>> consonance(allseg, 'Waldyr Azevedo')
    {False: 9.01639344262295, True: 90.98360655737704}
    """

    composerSegments = allSegmentsObj.getByComposer(composer).segments
    counterObj = Counter()

    for seg in composerSegments:
        myData = (intervals.is_consonant(i) for i in seg.intervals)
        counterObj = counterObj + Counter(myData)

    if percentage:
        counterObj = _utils.percentage(counterObj)

    return counterObj


def allLeaps(allSegmentsObj, composer, percentage=True):
    """Return a Counter dictionary with percentage values of all leaps
    classification of a given composer.

    >>> allLeaps(allseg, 'Waldyr Azevedo')
    """

    composerSegments = allSegmentsObj.getByComposer(composer).segments
    counterObj = Counter()

    for seg in composerSegments:
        myData = intervals.leaps(seg.intervals)
        counterObj = counterObj + Counter(myData)

    if percentage:
        counterObj = _utils.percentage(counterObj)

    return counterObj


def allIntervalsST(allSegmentsObj, composer, percentage=True):
    """Return a sequence with percentage values of all intervals in
    semitones classification of a given composer.

    >>> allIntervalsST(allseg, 'Waldyr Azevedo')
    [8, -1, -3, 1, 3, ... , 1, 1, 4, -1, 1, 4]
    """

    composerSegments = allSegmentsObj.getByComposer(composer).segments

    return _utils.flatten([seg.intervals_with_direction_semitones for seg in composerSegments])


def oscillation(allSegmentsObj, composer, percentage=True):
    """Return a sequence with percentage values of oscillation index
    classification of a given composer.

    >>> oscillation(allseg, 'Waldyr Azevedo')
    [8, -1, -3, 1, 3, ... , 1, 1, 4, -1, 1, 4]
    """

    composerSegments = allSegmentsObj.getByComposer(composer).segments

    return [seg.contour.oscillation_index() for seg in composerSegments]


def differentPoints(allSegmentsObj, composer, percentage=True):
    """Return a sequence with percentage values of oscillation index
    classification of a given composer.

    >>> oscillation(allseg, 'Waldyr Azevedo')
    [8, -1, -3, 1, 3, ... , 1, 1, 4, -1, 1, 4]
    """

    composerSegments = allSegmentsObj.getByComposer(composer).segments

    return contour.contour_different_cp(composerSegments)


def firstMovement(allSegmentsObj, composer, percentage=True):
    """Return a Counter dictionary with percentage values of first
    movement classification of a given composer.

    >>> firstMovement(allseg, 'Waldyr Azevedo')
    {1: 65.74074074074075, -1: 34.25925925925926}
    """

    composerSegments = allSegmentsObj.getByComposer(composer).segments
    counterObj = Counter()

    myData = contour.first_movement(composerSegments)

    if percentage:
        myData = _utils.percentage(myData)

    return myData


def lastMovement(allSegmentsObj, composer, percentage=True):
    """Return a Counter dictionary with percentage values of last
    movement classification of a given composer.

    >>> lastMovement(allseg, 'Waldyr Azevedo')
    {1: 32.407407407407405, -1: 67.5925925925926}
    """

    composerSegments = allSegmentsObj.getByComposer(composer).segments
    counterObj = Counter()

    myData = contour.last_movement(composerSegments)

    if percentage:
        myData = _utils.percentage(myData)

    return myData


def reductionBor355(allSegmentsObj, composer, percentage=True):

    composerSegments = allSegmentsObj.getByComposer(composer).segments

    coll = []
    for seg in composerSegments:
        myData = tuple(seg.contour.reduction_bor(355)[0])
        coll.append(myData)
    counterObj = Counter(coll)

    if percentage:
        counterObj = _utils.percentage(counterObj)

    return counterObj


def allDurations(allSegmentsObj, composer, percentage=True):
    composerSegments = allSegmentsObj.getByComposer(composer).segments
    counterObj = Counter()

    coll = []
    for seg in composerSegments:
        myData = duration.segmentDurations(seg)
        coll.extend(myData)
    counterObj = Counter(coll)

    if percentage:
        counterObj = _utils.percentage(counterObj)

    return counterObj


def allContourPrimeSimilarity(songsObj, composer):

    if composer == 'All composers':
        composerSongs = songsObj
    else:
        composerSongs = [songObj for songObj in songsObj if composer in songObj.composers]

    cPSimilarity = []
    totalLength = []

    for s in composerSongs:
        cPSimilarity.append(s.contourPrimeSimilarity)
        totalLength.append(sum([seg.totalLength for seg in s.segments]))

    return [cPSimilarity, totalLength]
