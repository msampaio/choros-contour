#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import _utils


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
