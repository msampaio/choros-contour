#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import _utils
import pickle
import song
import query


def save_pickle(typeof, filename, data):
    _utils.mkdir(os.path.join("data", typeof))
    with open(os.path.join("data", typeof, filename), 'w') as fileobj:
        pickle.dump(data, fileobj)


def load_pickle(typeof, filename):
    with open(os.path.join("data", typeof, filename)) as fileobj:
        return pickle.load(fileobj)


def run():
    # songs
    for coll in _utils.collections_list('choros-corpus'):
        print "Processing collection {0}...".format(coll)
        songs = song.makeSongCollection(coll, True)
        if songs:
            save_pickle('songs', coll, songs)
        else:
            print "No .form or .xml files in collection {0}".format(coll)

    # units
    print "Processing units...."
    save_pickle('units', 'units', query.makeAllMusicUnits(True))


if __name__ == '__main__':
    run()
