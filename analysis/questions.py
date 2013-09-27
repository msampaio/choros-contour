#!/usr/bin/env python
# -*- coding: utf-8 -*-


def __singleComparison(segmentsObj, mFilter, mStructure, value, exclusion=False):
    """Return a Counter object with the given mStructure filtered by a
    value filtered by mFilter.

    >>> __singleComparison(segmentsObj, 'getByComposerName', 'countIntervals', 'Pixinguinha')
    """

    return segmentsObj.__getattribute__(mFilter)(value, exclusion).__getattribute__(mStructure)()


def comparison(segmentsObj, mFilter, mStructure, *values):
    """Return a dictionary with data for each given value. The data is
    a counter object with the given mStructure filtered by the value
    filtered by mFilter.

    >>> comparison(segmentsObj, 'getByComposerName', 'countIntervals', 'Pixinguinha', 'Pecci', 'Nazareth')
    >>> comparison(segmentsObj, 'getByComposerBornYear', 'countIntervals', '1929')
    """

    dic = {}
    for value in values:
        dic[value] = __singleComparison(segmentsObj, mFilter, mStructure, value)
    return dic


def comparisonWithAll(segmentsObj, mFilter, mStructure, *values):
    """Return a dictionary with data for the given value and all. The
    data is a counter object with the given mStructure filtered by the
    value filtered by mFilter.

    >>> comparisonWithAll(segmentsObj, 'getByComposerName', 'countIntervals', 'Pixinguinha')
    """

    dic = comparison(segmentsObj, mFilter, mStructure, *values)
    dic['All'] = segmentsObj.__getattribute__(mStructure)()

    return dic


def comparisonWithOthers(segmentsObj, mFilter, mStructure, value):
    """Return a dictionary with data for the given value and others.
    The data is a counter object with the given mStructure filtered by
    the value filtered by mFilter.

    >>> comparisonWithOthers(segmentsObj, 'getByComposerName', 'countIntervals', 'Pixinguinha')
    """

    dic = {}
    dic[value] = __singleComparison(segmentsObj, mFilter, mStructure, value)
    dic['Others'] = __singleComparison(segmentsObj, mFilter, mStructure, value, True)

    return dic


def composersFrequency(segmentsObj):
    """Return a dictionary with frequency of composers segments."""

    dic = {}
    composers = segmentsObj.composers.composers
    for composer in composers:
        dic[composer] = segmentsObj.getByComposerName(composer).size

    return {'frequency': dic}
