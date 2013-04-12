#!/usr/bin/env python

import os
import sys
import re
import song


def get_songs_filenames(collections_dir):
    collections = os.listdir(collections_dir)
    if '.DS_Store' in collections:
        collections.remove('.DS_Store')

    pattern = '.*\.xml$'

    result = []
    for collection in collections:
        collpath = os.path.join(collections_dir, collection)
        files = os.listdir(collpath)
        songs = (os.path.join(collpath, re.search(pattern, f).string) for f in files if re.search(pattern, f))
        result.extend(songs)

    return result

if __name__ == '__main__':
    if (len(sys.argv) > 1):
        collections_dir = sys.argv[1]
        for f in get_songs_filenames(collections_dir):
            print "Processing {0}...".format(f)
            s = song.make_song(f, True)
            s.xml_write('numbered')
    else:
        print "Insert the correct corpus directory"
