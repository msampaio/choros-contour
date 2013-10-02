#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import _utils

CLASSES = ['Segment', 'Source', 'Collection', 'Piece', 'Composer',
           '_FormStructure', 'Form', 'Note', 'Interval']

class Structure(object):
    """Class for Structure objects. It's a super class for the classes
    Composer, Collection, Piece, Source and Segment."""

    def __init__(self):
        self.type = None

    def __eq__(self, other):
        return _utils.equalityComparisons(self, other)

    def __ne__(self, other):
        return _utils.equalityComparisons(self, other, True)

    def getAttrib(self, attribString):
        """Return the object's attribute from the attribstring.

        >>> Source().getAttrib('piece.composers')
        """

        obj = copy.deepcopy(self)
        args = attribString.split('.')
        for arg in args:
            if type(obj) == list and obj[0].check():
                obj = [singleObj.getAttrib(arg) for singleObj in obj]
                if len(obj) == 1:
                    obj = obj[0]
            else:
                obj = copy.deepcopy(obj.__getattribute__(arg))
        return obj

    def check(self, classes=CLASSES):
        """Returns True if the given object is a musical structure."""

        objectType = self.__class__.__name__
        # classes = ['Segment', 'Source', 'Collection', 'Piece', 'Composer',
        #            '_FormStructure', 'Form', 'Note', 'Interval']

        return objectType in classes
