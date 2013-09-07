#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import _utils

class IdCodeError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class IdCode(object):
    """Class for idCode objects."""
    
    def __init__(self):

        self.type = None
        self.collectionCode = None
        self.collectionVolume = None
        self.pieceNumber = None
        self.expansion = None
        self.pieceTitle = None
        self.idCode = None

    def __eq__(self, other):
        return _utils.equalityComparisons(self, other)

    def __ne__(self, other):
        return _utils.equalityComparisons(self, other, True)

    def __repr__(self):
        return "<idCode: {0}>".format(self.idCode)

    def check(self):
        """Check if idCode is valid."""

        conditions = [
            self.type in list('FT'),
            self.pieceNumber.isdigit(),
            not self.collectionVolume or self.collectionVolume.isdigit(),
            self.expansion in (True, False),
            not self.pieceTitle or ' ' not in self.pieceTitle,
            not (self.type == 'F' and self.expansion)
            ]

        if not all(conditions):
            raise IdCodeError('The given idCode is wrong.')

    def makeStringCode(self):
        """Return a string with the code."""

        prefix = ''.join([self.type, self.collectionCode])
        if self.collectionVolume:
            prefix = prefix + self.collectionVolume

        middle = self.pieceNumber
        if self.expansion:
            middle = middle + 'E'

        self.idCode = prefix + '_' + middle

        if self.pieceTitle:
            self.idCode = self.idCode + '-' + self.pieceTitle


def idCodeMaker(documentType, collectionCode, pieceNumber, expansion=False, collectionVolume=None, pieceTitle=None):
    """Return an idCode in a string.

    >>> idCodeMaker('T', 'MCB', '34', True, '1', 'Lamentos')
    'TMCB1_34E-Lamentos'
    """

    idCodeObj = IdCode()
    idCodeObj.type = documentType
    idCodeObj.collectionCode = collectionCode
    idCodeObj.collectionVolume = collectionVolume
    idCodeObj.pieceNumber = pieceNumber
    idCodeObj.expansion = expansion
    idCodeObj.pieceTitle = pieceTitle.replace(' ', '_')
    idCodeObj.makeStringCode()

    return idCodeObj


def idCodeParser(idCode):
    """Return a dictionary with idCode parsed.

    >>> idCodeParser('TMCB1_34E')
    {'expansion': True,
    'collectionCode': 'MCB',
    'collectionVolume': '1',
    'pieceNumber': '34',
    'type': 'T'}
    """

    splitted = idCode.split('-')

    idCodeObj = IdCode()
    idCodeObj.idCode = idCode

    if len(splitted) > 1:
        idCodeObj.pieceTitle = ' '.join(splitted[1:])
    else:
        idCodeObj.pieceTitle = None

    # FIXME: test if '_' exists
    pre, post = splitted[0].split('_')
    idCodeObj.type = pre[0]

    if pre[-1].isdigit():
        idCodeObj.collectionCode = pre[1:-1]
        idCodeObj.collectionVolume = pre[-1]
    else:
        idCodeObj.collectionCode = pre[1:]
        idCodeObj.collectionVolume = None

    if post[-1] == 'E':
        idCodeObj.expansion = True
        idCodeObj.pieceNumber = post[:-1]
    else:
        idCodeObj.expansion = False
        idCodeObj.pieceNumber = post

    try:
        idCodeObj.check()
        return idCodeObj
    except IdCodeError('Error'):
        print 'IdCode Error'


def getIdCodeByFilename(filename):
    """Return the idCode object from a given filename."""

    idCode = os.path.splitext(os.path.basename(filename))[0]
    return idCodeParser(idCode)
