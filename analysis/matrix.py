#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import copy
import _utils
import sift
import retrieval


class OutMatrix(object):
    """Class for output matrix objects."""

    def __init__(self):
        self.title = None
        self.rowsName = None
        self.rowsValues = None
        self.rowsValuesSet = None
        self.columnsName = None
        self.columnsValues = None
        self.columnsValuesSet = None

    def __repr__(self):
        return "<OutMatrix: {0}>".format(self.title)

    def nestedLists(self, invert=False):
        """Returns a list of lists with the object matrix. It's
        possible to invert the lists."""

        rValuesSet = copy.copy(self.rowsValuesSet)
        cValuesSet = copy.copy(self.columnsValuesSet)

        def aux(xValuesSet, yValuesSet, xDic):
            xOne = copy.copy(yValuesSet)
            xOne.insert(0, '')
            nestedList = [xOne]
            for xKey in xValuesSet:
                x = [xKey]
                x.extend([xDic[xKey][yKey] for yKey in yValuesSet])
                nestedList.append(x)
            return nestedList

        if invert:
            xDic = self.__getattribute__('columnsValues')
            xValuesSet = cValuesSet
            yValuesSet = rValuesSet
        else:
            xDic = self.__getattribute__('rowsValues')
            xValuesSet = rValuesSet
            yValuesSet = cValuesSet

        return aux(xValuesSet, yValuesSet, xDic)

    def csvSave(self, invert=False, path=None):
        """Save the object as a csv table."""

        if not path:
            path = '/tmp/umazero'
            _utils.mkdir(path)

        f = self.title.replace(' ', '_') + '.csv'
        filename = os.path.join(path, f)
        table = self.nestedLists(invert)
        _utils.saveCsvFile(table, filename)

    def transpose(self):
        """Return the OutMatrix with the matrix transposed."""

        outMatrix = OutMatrix()
        outMatrix.title = self.title
        outMatrix.rowsName = self.columnsName
        outMatrix.rowsValues = self.columnsValues
        outMatrix.rowsValuesSet = self.columnsValuesSet
        outMatrix.columnsName = self.rowsName
        outMatrix.columnsValues = self.rowsValues
        outMatrix.columnsValuesSet = self.rowsValuesSet

        return outMatrix


def makeOutMatrix(segmentsObj, nestedObj, getFn, attrib, countFn):
    """Returns an OutMatrix object."""

    def aux(segmentsObj, getFn, countFn, rowValue):
        return segmentsObj.__getattribute__(getFn)(rowValue)

    columnsName = countFn.replace('count', '')
    title = ' '.join([getFn.replace('getBy', ''), columnsName])

    rowsValues = {}
    columnsValues = {}
    columnsValuesSet = set()

    rowsName = attrib
    rowsValuesSet = segmentsObj.__getattribute__(nestedObj).__getattribute__(attrib)

    for rowValue in rowsValuesSet:
        seg = aux(segmentsObj, getFn, countFn, rowValue)
        cellData = seg.__getattribute__(countFn)()
        rowsValues[rowValue] = cellData
        columnsValuesSet.update(cellData.keys())

    for columnValue in columnsValuesSet:
        rowDic = {}
        for rowValue in rowsValuesSet:
            rowDic[rowValue] = rowsValues[rowValue][columnValue]
        columnsValues[columnValue] = rowDic

    outMatrix = OutMatrix()
    outMatrix.title = title
    outMatrix.rowsName = rowsName
    outMatrix.rowsValues = rowsValues
    outMatrix.rowsValuesSet = rowsValuesSet
    outMatrix.columnsName = columnsName
    outMatrix.columnsValues = columnsValues
    outMatrix.columnsValuesSet = sorted(list(columnsValuesSet))

    return outMatrix
