#!/usr/bin/env python

import os
import sys
import phrase
import _utils


def save_phrase(phr):
    filename = phr.filename
    number = phr.number
    print "Writing phrase {0}".format(number)

    phrase_filename = _utils.__path_without_extension(filename) + ' - phrase {0}.xml'.format(number)
    phr.score.write('musicxml', phrase_filename)


def save_phrases(path):
    filename = _utils.__path_without_extension(path)
    phrases = phrase.make_phrase(filename)
    [save_phrase(phr) for phr in phrases]

if __name__ == '__main__':
    if (len(sys.argv) > 1):
        filenames = sys.argv[1:]
        for f in filenames:
            save_phrases(f)
    else:
        print "Insert xml filename as argument:\npython enumerate foo.xml"
