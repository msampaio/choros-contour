#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import copy
import questions


def makeQuestion(fn, AllSegmentsObj, composersSeq, percentage=False, filename='/tmp/foo.csv'):
    """Run a given question function and save data in a given
    filename.
    """

    keys = set()
    values = {}
    composers = sorted(composersSeq)

    for composer in composers:
        dic = fn(allSegmentsObj, composer, percentage)
        for key in dic.keys():
            keys.add(key)
        values[composer] = dic

    sortedKeys = sorted(list(keys))
    with open(filename, 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)

        header = copy.deepcopy(sortedKeys)
        header.insert(0, u'Composer')
        spamwriter.writerow(header)

        for composer in composers:
            row = [composer]
            composerValues = values[composer]
            for k in sortedKeys:
                if k in composerValues:
                    v = composerValues[k]
                else:
                    v = 0
                row.append(v)
            spamwriter.writerow(row)


def runQuestions(allSegmentsObj, composersSeq):

    fnList = [questions.allIntervals,
              questions.stepLeapArpeggio,
              questions.consonance,
              questions.allLeaps,
              questions.firstMovement,
              questions.lastMovement,
              questions.reductionBor355,
              questions.allDurations]

    for fn in fnList:
        print fn
        makeQuestion(fn, allSegmentsObj, composersSeq, False, filename='/tmp/' + fn.func_name + '.csv')
