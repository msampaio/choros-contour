#!/usr/bin/env python

import os
import sys
import re
import song


def get_songs_filenames(collections_dir):
    collections = os.listdir(collections_dir)
    exclusion = ['.DS_Store', '.git', 'README.md']
    for ex in exclusion:
        if ex in collections:
            collections.remove(ex)

    pattern = '^((?!numbered).)*\.xml$'

    result = []
    for collection in collections:
        collpath = os.path.join(collections_dir, collection)
        files = os.listdir(collpath)
        songs = (os.path.join(collpath, re.search(pattern, f).string) for f in files if re.search(pattern, f))
        result.extend(songs)

    return result


def run(path):
    for f in get_songs_filenames(path):
        print "Processing {0}...".format(f)
        s = song.makeSong(f, True)
        s.xml_write('numbered')


if __name__ == '__main__':
    if (len(sys.argv) > 1):
        collections_dir = sys.argv[1]
        run(collections_dir)
    else:
        print "Insert the correct corpus directory"
