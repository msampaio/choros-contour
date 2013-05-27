#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json


class CollectionSong(object):
    """Class for song objects. This class is specific for the metadata
    organized in json file."""

    def __init__(self):

        self.title = None
        self.number = None
        self.collection = None
        self.composers = None
        self.composersStr = None

    def __repr__(self):
        return "<CollectionSong: {0} ({1}). {2}>".format(self.title, self.composersStr, self.collection)


class AllCollectionSongs(object):
    """Class for a set of CollectionSong objects. This class has
    attributes and methods to return information about CollectionSong
    objects parameters."""

    def __init__(self):

        self.collectionSongs = None
        self.allCollections = None
        self.allComposers = None
        self.allTitles = None
        self.number = None

    def __repr__(self):
        return "<AllCollectionSongs. Collections: {0}, Songs: {1}, Composers: {2}>".format(len(self.allCollections), self.number, len(self.allComposers))

    def getCollectionSong(self, collection, number):
        """Return a CollectionSong object from a given collection and
        file number. """

        for CollectionSongObj in self.collectionSongs:
            if CollectionSongObj.collection == collection and CollectionSongObj.number == number:
                return CollectionSongObj


def makeCollectionSong(jsonDic):
    """Return a CollectionSong object from an element."""

    collsong = CollectionSong()
    collsong.title = jsonDic['Title']
    collsong.number = jsonDic['Number']
    collsong.collection = jsonDic['Collection']
    composers = [jsonDic['Composer {0}'.format(i)] for i in range(1, 3)]
    collsong.composers = [c for c in composers if c != '']
    collsong.composersStr = ", ".join(composers)

    return collsong

def makeAllCollectionSongs(jsonSeq):
    """Return an AllCollectionSongs object from a sequence loaded from
    a json file."""

    allcollsongs = AllCollectionSongs()

    collections = set()
    composers = set()
    titles = set()
    collectionSongs = []
    for jsonDic in jsonSeq:
        collectionSong = makeCollectionSong(jsonDic)
        collectionSongs.append(collectionSong)
        collections.add(collectionSong.collection)
        for c in collectionSong.composers:
            composers.add(c)
        titles.add(collectionSong.title)
    allcollsongs.collectionSongs = collectionSongs
    allcollsongs.allCollections = sorted(collections)
    allcollsongs.allComposers = sorted(composers)
    allcollsongs.allTitles = sorted(titles)
    allcollsongs.number = len(collectionSongs)

    return allcollsongs


def loadSongCollections(filename='songs_map.json'):
    """Return an AllCollectionSongs object from a json file."""

    collectionsSeq = json.load(open(filename))
    return makeAllCollectionSongs(collectionsSeq)
