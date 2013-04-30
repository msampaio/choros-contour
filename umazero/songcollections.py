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
        self.composer = None
        self.lyrics = None

    def __repr__(self):
        return "<CollectionSong: {0} ({1}). {2}>".format(self.title, self.composer, self.collection)


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

def makeCollectionSong(jsonDic):
    """Return a CollectionSong object from an element."""

    collsong = CollectionSong()
    collsong.title = jsonDic['Title']
    collsong.number = jsonDic['Number']
    collsong.collection = jsonDic['Collection']
    collsong.composer = jsonDic['Composer']
    collsong.lyrics = jsonDic['Lyrics']

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
        composers.add(collectionSong.composer)
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
