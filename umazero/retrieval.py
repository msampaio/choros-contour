#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import _utils
import pickle
import song
import query
import files


def save_pickle(data, collection):
    """Save the given data in the file with collection names."""

    _utils.mkdir("data")
    with open(os.path.join("data", collection), 'w') as fileobj:
        pickle.dump(data, fileobj)


def load_pickle(collection):
    """Load pickle file with collection names."""

    with open(os.path.join("data", collection)) as fileobj:
        return pickle.load(fileobj)


def loadSongs(collection=None, path='choros-corpus'):
    """Load all Song objects saved in the pickle file from a given
    collection. If no collection is given, all collections data will
    be loaded."""

    if collection != None:
        return load_pickle(collection)
    else:
        songs = []
        collections = files.get_collections_names(path)
        for collection in collections:
            songs.extend(load_pickle(collection))
        return songs


def loadSegments(collection=None, path='choros-corpus'):
    """Load all Segment objects saved in the pickle file from a given
    collection. If no collection is given, all collections data will
    be loaded."""

    songs = loadSongs(collection, path)
    return query.makeAllSegmentsBySongSequence(songs, True)


def saveByCollection(collection, path='choros-corpus'):
    """Save pickle files for Song and Segment objects of all files in
    a given collection in 'choros-corpus' directory."""

    print 'Saving pickle of collection {0}...'.format(collection)
    songs = song.makeSongCollection(collection, True)
    save_pickle(songs, collection)


def saveAll(path='choros-corpus'):
    """Save pickle files for Song and Segment objects of all files in
    collections in 'choros-corpus' directory."""

    collections = files.get_collections_names(path)
    for collection in collections:
        saveByCollection(collection)


if __name__ == '__main__':
    saveAll()
