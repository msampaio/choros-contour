#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import _utils
import pickle
import song
import query


def save_pickle(typeof, data):
    """Save the given data in the file with typeof name."""

    _utils.mkdir("data")
    with open(os.path.join("data", typeof), 'w') as fileobj:
        pickle.dump(data, fileobj)


def load_pickle(typeof):
    """Load pickle file with name typeof."""

    with open(os.path.join("data", typeof)) as fileobj:
        return pickle.load(fileobj)


def loadSongs():
    """Load all Song objects saved in 'songs' pickle file"""

    return load_pickle('songs')


def loadMusicUnits():
    """Load all MusicUnits objects saved in 'units' pickle file"""

    return load_pickle('units')


def run():
    """Save pickle files for Song and MusicUnit objects of all files
    in collections in 'choros-corpus' directory."""

    # songs
    songs = []
    for coll in _utils.collections_list('choros-corpus'):
        print "Processing collection {0}...".format(coll)
        s = song.makeSongCollection(coll, True)
        if s:
            songs.extend(s)
        else:
            print "No .form or .xml files in collection {0}".format(coll)

    save_pickle('songs', songs)

    # Music Units
    print "Processing Music Units...."
    save_pickle('units', query.makeAllMusicUnits(True))


if __name__ == '__main__':
    run()
