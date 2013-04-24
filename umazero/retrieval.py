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
    """Load all Song objects saved in 'songs' pickle file."""

    return load_pickle('songs')


def loadSegments():
    """Load all Segments objects saved in 'segments' pickle file."""

    return load_pickle('segments')


def run():
    """Save pickle files for Song and Segment objects of all files in
    collections in 'choros-corpus' directory."""

    # songs
    songs = []
    for coll in _utils.filename_exclusion('choros-corpus'):
        print "Processing collection {0}...".format(coll)
        s = song.makeSongCollection(coll, True)
        if s:
            songs.extend(s)
        else:
            print "No .form or .xml files in collection {0}".format(coll)

    save_pickle('songs', songs)

    # Segments
    print "Processing Segments...."
    save_pickle('segments', query.makeAllSegments(True))


if __name__ == '__main__':
    run()
