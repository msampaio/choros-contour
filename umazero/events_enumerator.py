#!/usr/bin/env python

import os
import sys
import re
import song


def file_exclusion(path, exclusions=['.DS_Store', '.git', 'README.md']):
    files = os.listdir(path)
    for ex in exclusions:
        if ex in files:
            files.remove(ex)
    return files


def get_songs(path, pattern='^((?!numbered).)*\.xml$'):
    files = os.listdir(path)
    songs = (os.path.join(path, re.search(pattern, f).string) for f in files if re.search(pattern, f))
    return songs


def get_songs_filenames(collections_dir):
    exclusions = ['.DS_Store', '.git', 'README.md']
    pattern = '^((?!numbered).)*\.xml$'
    collections = file_exclusion(collections_dir, exclusions)

    result = []
    for collection in collections:
        songs = get_songs(os.path.join(collections_dir, collection), pattern)
        result.extend(songs)

    return result


def save(filename):
    print "Processing {0}...".format(filename)
    s = song.makeSong(filename, True)
    s.xml_write('numbered')


def enumerator(path):
    if os.path.isfile(path):
        save(path)
    else:
        songs = [x for x in get_songs(path)]
        if not songs:
            songs = get_songs_filenames(path)
        for f in songs:
            save(f)


if __name__ == '__main__':
    if (len(sys.argv) > 1):
        collections_dir = sys.argv[1]
        enumerator(collections_dir)
    else:
        print "Insert the correct corpus directory"
