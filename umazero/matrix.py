#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import Counter
import _utils
import query


def minoritiesRemotion(matrix, valuesCategories, valuesNumber):
    size = len(matrix)
    if size ==  valuesNumber:
        return matrix, valuesCategories
    else:
        valuesAndMatrix = zip(valuesCategories, [sum(els) for els in matrix], matrix)
        sortedValuesAndMatrix = sorted(valuesAndMatrix, reverse=True, key=lambda x:x[1])
        mostCommon = sortedValuesAndMatrix[:valuesNumber]
        other = tuple([sum(els) for els in zip(*[x[2] for x in sortedValuesAndMatrix[valuesNumber:]])])
        mostCommon.insert(0, ('Other', sum(other), other))

        newValuesCategories = []
        newMatrix = []

        for avalue, amount, amatrix in mostCommon:
            newValuesCategories.append(avalue)
            newMatrix.append(amatrix)

        return newMatrix, newValuesCategories


def appendMatrix(matrix, values, valuesCategories):
    """Insert a row of values in a given matrix

    >>> appendMatrix([], [True, True, False], ['True', 'False'])
    [[33.333333333333336, 66.66666666666667, 0, 0]]
    """

    # values in _utils.percentage
    counted = _utils.percentage(Counter(values))
    composerValuesCategories = counted.keys()

    for valueCategory in valuesCategories:
        if valueCategory not in composerValuesCategories:
            counted[valueCategory] = 0

    categoryAndValueSeq = sorted(counted.items())
    matrix.append([value for category, value in categoryAndValueSeq])

    return matrix


def makeAttribValuesSequence(allSegmentObj, composer, attrib):
    """Return a sequence of attribute values from a given composer and
    attribute.

    # allseg is a query.AllSegments object

    >>> makeAttribValuesSequence(allseg, 'Pixinguinha', 'meter')
    [Duple', 'Duple', 'Triple', ... , 'Duple', 'Duple']
    """

    composerSegmentsSeq = allSegmentObj.getByComposer(composer).segments

    if attrib in ('contour', 'contour_prime'):
        values = [tuple(getattr(seg, attrib)) for seg in composerSegmentsSeq]
    else:
        values = [getattr(seg, attrib) for seg in composerSegmentsSeq]

    return values


def appendAttribMatrix(matrix, allSegmentObj, composer, attrib, valuesCategories):
    """Make a sequence of attribute values and append it to a given matrix

    # allseg is a query.AllSegments object

    >>> appendAttribMatrix([], allseg, 'Pixinguinha', 'pickup', ['True', 'False'])
    [[25.617977528089888, 74.38202247191012, 0, 0]]
    """

    values = makeAttribValuesSequence(allSegmentObj, composer, attrib)

    return appendMatrix(matrix, values, valuesCategories)


def makeAttribValuesMatrix(allSegmentsObj, attrib, allAndTopComposers, contourType=False):
    """Return a matrix with data to plot in stackedBar chart, and a
    sequence with the values categories.

    >>> makeAttribValuesMatrix(allseg, 'meter', ['All composers', u'Benedito Lacerda', u'Ernesto Nazareth'])

    ([[97.2508591065292, 0.9163802978235968, 1.8327605956471935], [100.0, 0, 0], [100.0, 0, 0]],
    ['Duple', 'Quadruple', 'Triple'])
    """

    matrix = []
    valuesCategories = query.getData(allSegmentsObj.segments, attrib)

    if contourType:
        valuesCategories = [tuple(cseg) for cseg in valuesCategories]

    for composer in allAndTopComposers:
        matrix = appendAttribMatrix(matrix, allSegmentsObj, composer, attrib, valuesCategories)

    return matrix, valuesCategories


def makeMatrix(matrix, allAndTopComposers, valuesCategories, valuesNumber, contourType=False):
    """Transpose a given matrix and return also a sequence of values
    categories and all and top composers.

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

    newMatrix, newValuesCategories = minoritiesRemotion(transposedMatrix, valuesCategories, valuesNumber)

    if contourType:
        from music21.contour.contour import Contour
        newValuesCategories = _utils.flatten([[newValuesCategories[0]], [Contour(cseg) for cseg in newValuesCategories[1:]]])

    return newMatrix, newValuesCategories, allAndTopComposers


def attribValuesMatrix(allSegmentsObj, topComposers, attrib, valuesNumber=5):
    """Return a Sequence with a Matrix of attribute values, all
    attribute values and top composers."""

    if attrib in ('contour', 'contour_prime'):
        contourType = True
    else:
        contourType = False

    allAndTopComposers = _utils.flatten([['All composers'], topComposers])
    attribMatrix, valuesCategories = makeAttribValuesMatrix(allSegmentsObj, attrib, allAndTopComposers, contourType)

    return makeMatrix(attribMatrix, allAndTopComposers, valuesCategories, valuesNumber, contourType)
