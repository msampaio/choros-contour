#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import Counter
import _utils
import intervals


def allIntervals(allSegmentObj, composer):
    """Return a Counter dictionary with percentage values of all
    intervals classification of a given composer.

    >>> allIntervals(allseg, 'Waldyr Azevedo')
    {'m10': 1.2170889220069547, 'M7': 0.07451564828614009, ... , 'M10': 0.024838549428713365, 'AA1': 0.09935419771485346}
    """

    composerSegments = allSegmentObj.getByComposer(composer).segments
    counterObj = Counter()

    for seg in composerSegments:
        myData = seg.intervals
        counterObj = counterObj + Counter(myData)

    return _utils.percentage(counterObj)


def stepLeapArpeggio(allSegmentObj, composer):
    """Return a Counter dictionary with percentage values of all
    steps, leaps and arpeggios classification of a given composer.

    >>> stepLeapArpeggio(allseg, 'Waldyr Azevedo')
    {'Leap': 21.609538002980624, 'Repetition': 8.917039244908098, 'Step': 47.66517635370094, '3rd': 21.808246398410333}
    """

    composerSegments = allSegmentObj.getByComposer(composer).segments
    counterObj = Counter()

    for seg in composerSegments:
        myData = intervals.step_leap_arpeggio(seg.intervals)
        counterObj = counterObj + Counter(myData)

    return _utils.percentage(counterObj)


def consonance(allSegmentObj, composer):
    """Return a Counter dictionary with percentage values consonance
    intervals classification of a given composer.

    >>> consonance(allseg, 'Waldyr Azevedo')
    {False: 9.01639344262295, True: 90.98360655737704}
    """

    composerSegments = allSegmentObj.getByComposer(composer).segments
    counterObj = Counter()

    for seg in composerSegments:
        myData = (intervals.is_consonant(i) for i in seg.intervals)
        counterObj = counterObj + Counter(myData)

    return _utils.percentage(counterObj)


def allLeaps(allSegmentObj, composer):
    """Return a Counter dictionary with percentage values of all leaps
    classification of a given composer.

    >>> allLeaps(allseg, 'Waldyr Azevedo')
    """

    composerSegments = allSegmentObj.getByComposer(composer).segments
    counterObj = Counter()

    for seg in composerSegments:
        myData = intervals.leaps(seg.intervals)
        counterObj = counterObj + Counter(myData)

    return _utils.percentage(counterObj)
