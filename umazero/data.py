#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import _utils
import pickle
import song


def save_pickle(typeof, filename, data):
    _utils.mkdir(os.path.join("data", typeof))
    with open(os.path.join("data", typeof, filename), 'w') as fileobj:
        pickle.dump(data, fileobj)


def load_pickle(typeof, filename):
    with open(os.path.join("data", typeof, filename)) as fileobj:
        return pickle.load(fileobj)


def run():
    for coll in _utils.collections_list('choros-corpus'):
        print "Processing collection {0}...".format(coll)
        coll_data = song.makeSongCollection(coll, True)
        if coll_data:
            save_pickle('songs', coll, coll_data)
        else:
            print "No .form or .xml files in collection {0}".format(coll)


if __name__ == '__main__':
    run()
