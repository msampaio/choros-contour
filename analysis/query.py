#!/usr/bin/env python
# -*- coding: utf-8 -*-

import core
import _utils
import auxiliar
import structure


class QueryError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Query(object):
    """Class of Query objects."""

    def __init__(self):
        self.objects = None
        self.number = None
        self.type = None

    def __repr__(self):
        return "<Query: {0} objects {1}>".format(self.number, self.type)

    def getAttrib(self, attribString, counter=False):
        """Return the object's attribute from the attribstring.

        >>> query.getAttrib('piece.composer')
        """

        args = attribString.split('.')
        objects = [obj.getAttrib(attribString) for obj in self.objects]

        r = []
        for obj in objects:
            if type(obj) == list:
                r.extend(obj)
            else:
                r.append(obj)
        objects = r
        objExample = objects[0]
        if type(objExample) in ['str', 'int']:
            if objExample.check():
                objects = makeQuery(objects)
        elif counter:
            objects = auxiliar.makeExtCounter(objects, args[-1], args[0])
        return objects

    def query(self, attribString, value, exclusion=False):
        """Returns a Query object with the values that the given value
        is in or equal to their attribString values.

        >>> query.query('piece.composers.name', 'Pixinguinha')
        """

        return [obj for obj in self.objects if _utils.testInEqual(value, obj.getAttrib(attribString), exclusion)]

    def check(self):
        """Check if the Query object is valid."""

        types = list(set([obj.__class__.__name__ for obj in self.objects]))
        classes = ['Segment', 'Source', 'Collection', 'Piece', 'Composer']
        if not (len(types) == 1 and types[0] in core.CLASSES):
            raise QueryError('Error in the given structures types.')
        else:
            self.types = types[0]


def makeQuery(structureObjects):
    """Returns a Query object from a given sequence of structure
    objects."""

    query = Query()
    query.objects = structureObjects
    query.number = len(query.objects)

    try:
        query.check()
        return query
    except QueryError('Error'):
        print 'Query Error'
