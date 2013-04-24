#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json


class CollectionSong(object):
    """Class for song objects. This class is specific for the metadata
    organized in json file."""

    def __init__(self, dic):

        self.title = dic['Title']
        self.number = dic['Number']
        self.collection = dic['Collection']
        self.composer = dic['Composer']
        self.lyrics = dic['Lyrics']

    def __repr__(self):
        return "<CollectionSong: {0} ({1}). {2}>".format(self.title, self.composer, self.collection)


class AllCollectionSongs(object):
    """Class for a set of CollectionSong objects. This class has
    attributes and methods to return information about CollectionSong
    objects parameters."""

    def __init__(self, dic):

        self.collectionSongs = dic['collectionSongs']
        self.allCollections = dic['allCollections']
        self.allComposers = dic['allComposers']
        self.allTitles = dic['allTitles']
        self.number = dic['number']

    def __repr__(self):
        return "<AllCollectionSongs. Collections: {0}, Songs: {1}, Composers: {2}>".format(len(self.allCollections), self.number, len(self.allComposers))


def makeAllCollectionSongs(jsonSeq):
    """Return an AllCollectionSongs object from a sequence loaded from
    a json file."""

    dic = {}

    collections = set()
    composers = set()
    titles = set()
    collectionSongs = []
    for el in jsonSeq:
        collectionSongs.append(CollectionSong(el))
        collections.add(el['Collection'])
        composers.add(el['Composer'])
        titles.add(el['Title'])
    dic['collectionSongs'] = collectionSongs
    dic['allCollections'] = sorted(collections)
    dic['allComposers'] = sorted(composers)
    dic['allTitles'] = sorted(titles)
    dic['number'] = len(collectionSongs)

    return AllCollectionSongs(dic)


def loadSongCollections(filename='songs_map.json'):
    """Return an AllCollectionSongs object from a json file."""

    collectionsSeq = json.load(open(filename))
    return makeAllCollectionSongs(collectionsSeq)
