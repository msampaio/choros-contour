#!/usr/bin/env python
# -*- coding: utf-8 -*-


def compareComposers(segmentsObj, method, *composers):
    """Return the data of a given list of composers.

    >>> compareComposers(segmentsObj, 'countIntervals', 'Pixinguinha', 'Pecci', 'Nazareth')
    """

    def aux(segmentsObj, method, composer):
        dic[composer] = segmentsObj.getByComposerName(composer).__getattribute__(method)()

    dic = {}
    for composer in composers:
        aux(segmentsObj, method, composer)
    return dic


def compareComposerWithAll(segmentsObj, method, composerName):
    """Return the data of a given list of composers.

    >>> compareComposersWithAll(segmentsObj, 'countIntervals', 'Pixinguinha')
    """

    dic = {}
    dic[composerName] = segmentsObj.getByComposerName(composerName).__getattribute__(method)()
    dic['All composers'] = segmentsObj.__getattribute__(method)()

    return dic


def compareComposerWithOthers(segmentsObj, method, composerName):
    """Return the data of a given list of composers.

    >>> compareComposersWithOthers(segmentsObj, 'countIntervals', 'Pixinguinha')
    """

    dic = {}
    dic[composerName] = segmentsObj.getByComposerName(composerName).__getattribute__(method)()
    dic['Others'] = segmentsObj.getByComposerName(composerName, True).__getattribute__(method)()

    return dic


def composersFrequency(segmentsObj):
    """Return a dictionary with frequency of composers segments."""

    dic = {}
    composers = segmentsObj.composers.composers
    for composer in composers:
        dic[composer] = segmentsObj.getByComposerName(composer).size

    return {'frequency': dic}
