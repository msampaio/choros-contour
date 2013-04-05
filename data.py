#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import _utils
import pickle
import phrase


def save_pickle(filename, data):
    with open(os.path.join("data", filename), 'w') as fileobj:
        pickle.dump(data, fileobj)


def load_pickle(filename):
    with open(os.path.join("data", filename)) as fileobj:
        return pickle.load(fileobj)


if __name__ == '__main__':
    _utils.mkdir('data')
    for coll in _utils.collections_list('choros-corpus'):
        print "Processing collection {0}...".format(coll)
        coll_data = phrase.make_phrase_collection(coll, False)
        if coll_data:
            save_pickle(coll, coll_data)
        else:
            print "No .phrase or .xml phrases in collection {0}".format(coll)
