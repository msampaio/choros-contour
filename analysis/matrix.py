#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import copy
import _utils
import sift


def countedToCsv(dic, filename='/tmp/foo.csv'):
    """Save a given dictionary in a given csv file."""

    header = dic.keys()
    rowOne = set()
    for countObj in dic.values():
        for key in countObj.keys():
            rowOne.add(key)
    rowOne = sorted(list(rowOne))

    csvTable = [copy.deepcopy(header)]
    csvTable[0].insert(0, '')
    for r in rowOne:
        csvRow = [r]
        for h in header:
            csvRow.append(dic[h][r])
        csvTable.append(csvRow)

    _utils.saveCsvFile(csvTable, filename)

def makeStatisticalTables(segmentsObj=None):

    if not segmentsObj:
        segmentObjs = retrieval.loadPickle('Segment')
        segmentsObj = sift.makeSegments(segmentObjs)

    countedSeq = ['countIntervals', 'countFirstIntervals', 'countLastIntervals',
                  'countContourPrimes', 'countMeasuresNumbers', 'countAmbitus',
                  'countMeter', 'countTimeSignature']

    countedData = {}
    for fn in countedSeq:
        print 'Processing {0}'.format(fn)
        cData = sift.makeMatrix(segmentsObj, 'getByComposerName', 'composers', fn)
        countedToXls(cData, os.path.join('/tmp', fn + '.csv'))
