#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _utils
import idcode
import parse


class City(object):
    """Class for City objects."""
    
    def __init__(self):

        self.name = None
        self.province = None

    def __eq__(self, other):
        return _utils.equalityComparisons(self, other)

    def __ne__(self, other):
        return _utils.equalityComparisons(self, other, True)

    def __repr__(self):
        return "<City: {0}, {1}>".format(self.name, self.province)


class Composer(object):
    """Class for Composer objects."""
    
    def __init__(self):

        self.name = None
        self.gender = None
        self.bornCity = None
        self.bornYear = None
        self.deathCity = None
        self.deathYear = None
        self.mainInstrument = None

    def __eq__(self, other):
        return _utils.equalityComparisons(self, other)

    def __ne__(self, other):
        return _utils.equalityComparisons(self, other, True)

    def __repr__(self):
        if self.bornCity:
            bornCity = self.bornCity.province
        else:
            bornCity = None

        return "<Composer: {0}, {1}, {2}--{3}>".format(self.name, bornCity, self.bornYear, self.deathYear)


class Piece(object):
    """Class for Piece objects."""

    def __init__(self):

        self.title = None
        self.subtitle = None
        self.composer = None
        self.city = None
        self.year = None

    def __eq__(self, other):
        return _utils.equalityComparisons(self, other)

    def __ne__(self, other):
        return _utils.equalityComparisons(self, other, True)

    def __repr__(self):
        return "<Piece: {0} ({1})>".format(self.title, self.makeComposersString())

    def makeComposersString(self):
        return ', '.join([composer.completeName() for composer in self.composer])


class Collection(object):
    """Class for Collection objects."""

    def __init__(self):

        self.title = None
        self.author = None
        self.publisher = None
        self.volume = None
        self.code = None

    def __eq__(self, other):
        return _utils.equalityComparisons(self, other)

    def __ne__(self, other):
        return _utils.equalityComparisons(self, other, True)

    def __repr__(self):
        return "<Collection: {0}, vol.{1}>".format(self.title, self.volume)

    def makeCollectionCode(self):
        """Return a string with the collection code."""

        initials = [word[0] for word in self.title.split(' ') if word[0].isupper()]
        self.code = ''.join(initials)
    

class Source(object):
    """Class for Source objects."""

    def __init__(self):

        self.piece = None
        self.collection = None
        self.idCode = None
        self.filename = None
        self.formSeq = None
        self.score = None

    def __eq__(self, other):
        return _utils.equalityComparisons(self, other)

    def __ne__(self, other):
        return _utils.equalityComparisons(self, other, True)

    def __repr__(self):
        return "<Source: {0}, {1}>".format(self.piece.title, self.idCode.idCode)

    def makeScore(self):
        """Create a Music21 stream object in score attribute."""

        if not self.score:
            self.score = parse.sourceParse(self.filename)


def makeCity(name, province):
    """Return a City object with the given attributes."""

    city = City()
    city.name = name
    city.province = province

    return city


def makeComposer(name, gender='M', bornCityObj=None, bornYear=None, deathCityObj=None, deathYear=None, mainInstrument=None):
    """Return a Composer object with the given attributes. The year
    must be an integer."""

    composer = Composer()
    composer.name = name
    composer.gender = gender
    composer.bornCity = bornCityObj
    composer.deathCity = deathCityObj
    composer.mainInstrument = mainInstrument
    composer.bornYear = bornYear
    composer.deathYear = deathYear

    return composer


def makePiece(title, composer, year=None, subtitle=None, city=None):
    """Return a Piece object with the given attributes. The year must
    be an integer such as 1977."""

    piece = Piece()

    piece.title = title
    piece.year = year
    piece.subtitle = subtitle
    piece.composer = composer
    piece.city = city

    return piece


def makeCollection(title, authorList, publisher, volume=None):
    """Return a Collection object with the given attributes."""

    collection = Collection()
    
    collection.title = title
    collection.author = authorList
    collection.publisher = publisher
    collection.volume = volume
    collection.makeCollectionCode()

    return collection


def makeSource(pieceObj, collectionObj, filename=None):
    """Return a Source object with the given attributes."""

    source = Source()

    source.piece = pieceObj
    source.collection = collectionObj
    if filename:
        source.filename = filename
        source.idCode = idcode.getIdCodeByFilename(filename)
        source.score = parse.sourceParse(filename)
        source.formSeq = parse.formParse(filename)

    return source
