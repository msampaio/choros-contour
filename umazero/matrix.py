#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import Counter
import _utils
import query
from music21.contour import Contour


def minoritiesRemotion(matrix, valuesSet, valuesNumber):
    size = len(matrix)
    if size ==  valuesNumber:
        return matrix, valuesSet
    else:
        valuesAndMatrix = zip(valuesSet, [sum(els) for els in matrix], matrix)
        sortedValuesAndMatrix = sorted(valuesAndMatrix, reverse=True, key=lambda x:x[1])
        mostCommon = sortedValuesAndMatrix[:valuesNumber]
        other = tuple([sum(els) for els in zip(*[x[2] for x in sortedValuesAndMatrix[valuesNumber:]])])
        mostCommon.insert(0, ('Other', sum(other), other))

        newValuesSet = []
        newMatrix = []

        for avalue, amount, amatrix in mostCommon:
            newValuesSet.append(avalue)
            newMatrix.append(amatrix)

        return newMatrix, newValuesSet


def appendMatrix(matrix, valuesSeq, valuesSet):
    """Insert a row of values in a given matrix

    >>> appendMatrix([], [True, True, False], ['True', 'False'])
    [[33.333333333333336, 66.66666666666667, 0, 0]]
    """

    # values in _utils.percentage
    counted = _utils.percentage(Counter(valuesSeq))
    composerValuesSet = counted.keys()

    for value in valuesSet:
        if value not in composerValuesSet:
            counted[value] = 0

    setElementAndValueSeq = sorted(counted.items())
    matrix.append([value for element, value in setElementAndValueSeq])

    return matrix


def makeAttribValuesSequence(allSegmentsObj, composer, attrib):
    """Return a sequence of attribute values from a given composer and
    attribute.

    # allseg is a query.AllSegments object

    >>> makeAttribValuesSequence(allseg, 'Pixinguinha', 'meter')
    [Duple', 'Duple', 'Triple', ... , 'Duple', 'Duple']
    """

    composerSegmentsSeq = allSegmentsObj.getByComposer(composer).segments

    if attrib in ('contour', 'contour_prime'):
        valuesSeq = [tuple(getattr(seg, attrib)) for seg in composerSegmentsSeq]
    else:
        valuesSeq = [getattr(seg, attrib) for seg in composerSegmentsSeq]

    return valuesSeq


def appendAttribMatrix(matrix, allSegmentsObj, composer, attrib, valuesSet):
    """Make a sequence of attribute values and append it to a given matrix

    # allseg is a query.AllSegments object

    >>> appendAttribMatrix([], allseg, 'Pixinguinha', 'pickup', ['True', 'False'])
    [[25.617977528089888, 74.38202247191012, 0, 0]]
    """

    valuesSeq = makeAttribValuesSequence(allSegmentsObj, composer, attrib)

    return appendMatrix(matrix, valuesSeq, valuesSet)


def makeAttribValuesMatrix(allSegmentsObj, attrib, allAndTopComposers, contourType=False):
    """Return a matrix with data to plot in stackedBar chart, and a
    sequence with the values set.

    >>> makeAttribValuesMatrix(allseg, 'meter', ['All composers', u'Benedito Lacerda', u'Ernesto Nazareth'])

    ([[97.2508591065292, 0.9163802978235968, 1.8327605956471935], [100.0, 0, 0], [100.0, 0, 0]],
    ['Duple', 'Quadruple', 'Triple'])
    """

    matrix = []
    valuesSet = query.getData(allSegmentsObj.segments, attrib)

    if contourType:
        valuesSet = [tuple(cseg) for cseg in valuesSet]

    for composer in allAndTopComposers:
        matrix = appendAttribMatrix(matrix, allSegmentsObj, composer, attrib, valuesSet)

    return matrix, valuesSet


def makeDataValuesMatrix(allSegmentsObj, allAndTopComposers, fn):
    """Return a matrix with data to plot in stackedBar chart, and a
    sequence with the values set.

    >>> makeDataValuesMatrix(allseg, ['All composers', u'Benedito Lacerda', u'Ernesto Nazareth'], intervals.allIntervals)

    ([0.02737401111384851, 0.13550135501355012, 0.20667378390955626,...,0, 0, 0, 0, 0, 0]],
    ['d8', 'm10', 'M7', ... , 'M13', 'AA1', 'M14'])
    """

    def makeRowFromDic(dic, keys):
        row = []
        for key in keys:
            if key in dic:
                row.append(dic[key])
            else:
                row.append(0)
        return row

    dicSeq = [fn(allSegmentsObj, composer) for composer in allAndTopComposers]

    valuesSet = dicSeq[0].keys()
    myMatrix = []

    for d in dicSeq:
        myMatrix.append(makeRowFromDic(d, valuesSet))

    return myMatrix, valuesSet


def makeMatrix(matrix, allAndTopComposers, valuesSet, valuesNumber, contourType=False):
    """Transpose a given matrix and return also a sequence of values
    set and all and top composers.

    >>> matrix = [[97.2508591065292, 0.9163802978235968, 1.8327605956471935],
                  [100.0, 0, 0],
                  [100.0, 0, 0]]
    >>> allAndTopComposers = ['All composers', u'Benedito Lacerda', u'Ernesto Nazareth']
    >>> makeMatrix(matrix, ['Duple', 'Quadruple', 'Triple'], 3, False)
    ([(97.2508591065292, 100.0, 100.0), (0.9163802978235968, 0, 0), (1.8327605956471935, 0, 0)],
    ['Duple', 'Quadruple', 'Triple'],
    ['All composers', u'Benedito Lacerda', u'Ernesto Nazareth'])
    """

    size = len(matrix)
    transposedMatrix = zip(*matrix)

    newMatrix, newValuesSet = minoritiesRemotion(transposedMatrix, valuesSet, valuesNumber)

    if contourType:
        from music21.contour.contour import Contour
        newValuesSet = _utils.flatten([[newValuesSet[0]], [Contour(cseg) for cseg in newValuesSet[1:]]])

    return newMatrix, newValuesSet, allAndTopComposers


def attribValuesMatrix(allSegmentsObj, topComposers, attrib, valuesNumber=5):
    """Return a Sequence with a Matrix of attribute values, all
    attribute values and top composers."""

    if attrib in ('contour', 'contour_prime'):
        contourType = True
    else:
        contourType = False

    allAndTopComposers = _utils.flatten([['All composers'], topComposers])
    attribMatrix, valuesSet = makeAttribValuesMatrix(allSegmentsObj, attrib, allAndTopComposers, contourType)

    return makeMatrix(attribMatrix, allAndTopComposers, valuesSet, valuesNumber, contourType)


def dataValuesMatrix(allSegmentsObj, allAndTopComposers, fn, valuesNumber=5, contourType=False):
    """Return a Sequence with a Matrix of attribute values, all
    attribute values and top composers."""

    fnMatrix, valuesSet = makeDataValuesMatrix(allSegmentsObj, allAndTopComposers, fn)

    return makeMatrix(fnMatrix, allAndTopComposers, valuesSet, valuesNumber, contourType)
