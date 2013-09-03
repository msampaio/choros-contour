#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _utils
import idcode


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
        self.prename = None
        self.nickname = None
        self.gender = None
        self.bornCity = None
        self.bornDate = None
        self.deathCity = None
        self.deathDate = None
        self.mainInstrument = None

    def __eq__(self, other):
        return _utils.equalityComparisons(self, other)

    def __ne__(self, other):
        return _utils.equalityComparisons(self, other, True)

    def __repr__(self):
        if self.bornDate:
            bornDate = self.bornDate.year
        else:
            bornDate = None

        if self.deathDate:
            deathDate = self.deathDate.year
        else:
            deathDate = None

        if self.bornCity:
            bornCity = self.bornCity.province
        else:
            bornCity = None

        return "<Composer: {0}, {1}, {2}--{3}>".format(self.name, bornCity, bornDate, deathDate)

    def completeName(self):
        return ' '.join([self.prename, self.name])


class Piece(object):
    """Class for Piece objects."""

    def __init__(self):

        self.title = None
        self.subtitle = None
        self.composer = None
        self.city = None
        self.date = None

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

    def __eq__(self, other):
        return _utils.equalityComparisons(self, other)

    def __ne__(self, other):
        return _utils.equalityComparisons(self, other, True)

    def __repr__(self):
        return "<Source: {0}, {1}>".format(self.piece.title, self.idCode)


def makeCity(name, province):
    """Return a City object with the given attributes."""

    city = City()
    city.name = name
    city.province = province

    return city


def makeComposer(completeName, nickname=None, gender='M', bornCityObj=None, bornDate=None, deathCityObj=None, deathDate=None, mainInstrument=None):
    """Return a Composer object with the given attributes. The dates
    must be in a string with the format YYYYMMDD."""

    composer = Composer()
    composer.prename, composer.name = _utils.nameParser(completeName)
    composer.nickname = nickname
    composer.gender = gender
    composer.bornCity = bornCityObj
    composer.deathCity = deathCityObj
    composer.mainInstrument = mainInstrument

    if bornDate:
        composer.bornDate = _utils.dateParser(bornDate)
    if deathDate:
        composer.deathDate = _utils.dateParser(deathDate)

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


def makeSource(pieceObj, collectionObj, idCode):
    """Return a Source object with the given attributes."""

    source = Source()
    
    source.piece = pieceObj
    source.collection = collectionObj
    source.idCode = idCode
        
    try:
        idcode.idCodeParser(idCode)
        return source
    except idcode.IdCodeError('Error'):
        print 'IdCode Error'
