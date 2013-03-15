#!/usr/bin/env python

import os
import sys
import core


def save_phrase(phrase):
    filename = phrase.filename
    number = phrase.number
    print "Writing phrase {0}".format(number)

    phrase_filename = core.__path_without_extension(filename) + ' - phrase {0}.xml'.format(number)
    phrase.score.write('musicxml', phrase_filename)


def save_phrases(path):
    filename = core.__path_without_extension(path)
    phrases = core.make_phrase_obj(filename)
    [save_phrase(phrase) for phrase in phrases]

if __name__ == '__main__':
    if (len(sys.argv) > 1):
        filenames = sys.argv[1:]
        for f in filenames:
            save_phrases(f)
    else:
        print "Insert xml filename as argument:\npython enumerate foo.xml"
