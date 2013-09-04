#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import os
import unicodedata
import csv
import json


def dateParser(dateString):
    """Return a datetime object from a dateString argument in
    format YYYYMMDD."""

    y, m, d = [int(s) for s in dateString[:4], dateString[4:6], dateString[6:]]
    return datetime.date(y, m, d)


def nameParser(completeNameStr):
    """Return prename and name in two separate strings."""

    names = completeNameStr.split()
    if names[-1] == 'Jr.':
        return ' '.join(names[:-2]), ' '.join(names[-2:])
    else:
        return ' '.join(names[:-1]), names[-1:][0]


def equalityComparisons(objectOne, objectTwo, inequality=False):
    attribList = objectOne.__dict__.keys()
    if objectOne.__dict__.keys() != objectTwo.__dict__.keys():
        return False
    else:
        comparisons = []
        if objectOne and objectTwo:
            for method in ['__class__', '__dict__']:
                methodOne = getattr(objectOne, method)
                methodTwo = getattr(objectTwo, method)
                comparisons.append(methodOne == methodTwo)
            for atrb in attribList:
                atrbOne = objectOne.__getattribute__(atrb)
                atrbTwo = objectTwo.__getattribute__(atrb)
                comparisons.append(atrbOne == atrbTwo)
        else:
            comparisons.append(False)
        if inequality:
            return not all(comparisons)
        else:
            return all(comparisons)


def csvToJson(filename):
    dirname = os.path.dirname(filename)
    basename = os.path.basename(filename)
    baseprename = os.path.splitext(basename)[0]
    jsonname = os.path.join(dirname, baseprename + '.json')

    with open(filename, 'r') as csvfile:
        fieldnames = csvfile.readline().strip('\n').split(';')[:-1]
        reader = csv.DictReader(csvfile, fieldnames = tuple(fieldnames), delimiter=';')
        out = []
        for row in reader:
            del row[None]
            out.append(row)

    with open(jsonname, 'w') as jsonfile:
        jsonfile.write(json.dumps(out, indent=4))


def unicodeNormalize(string):
    """Return a normalized string. It's useful to process filenames
    with special characters."""

    new_string = unicodedata.normalize('NFKD', unicode(string)).encode('ascii', 'ignore')
    return new_string.replace(',', '').replace('?', '').replace('(', '').replace(')', '').replace(' ', '_')


