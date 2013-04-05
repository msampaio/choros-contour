#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
from collections import Counter
import _utils
import data

class WebpageError(Exception):
    pass


def rst_header(title, level=1):
    levels = u"* = - ^".split()

    if level > 4 or level < 1:
        raise WebpageError("We have levels from 1 to 4")

    header = levels[level - 1] * len(title)
    return u"{0}\n{1}\n\n".format(title, header)


def rst_image(filename, directory, scale_factor=100):
    return u".. image:: {0}/{1}.png\n   :scale: {2}\n".format(directory, filename, scale_factor)


def rst_table(dic, size=8):
    mark = "{0} {0}".format("=" * size)
    result = [mark]
    for key, val in _utils.sort2(dic):
        result.append("{1:{0}} {2:{0}.2f}".format(size, key, val))
    result.append(mark)
    return "\n".join(result)


def print_attribute(attribute, collection, out):
    counter = Counter([getattr(song, attribute) for song in collection])
    out.write(rst_table(_utils.percentage(counter)))
    out.write("\n\n")


def make_basic_data_webpage(alist):

    def print_data(composer, phrases):
            print "Processing phrases of composer... {0}".format(composer)

            songs_number = _utils.count_songs_from_phrases(phrases)

            out.write(rst_header(composer, 2))

            out.write("Number of Songs: {0}\n\n".format(songs_number))
            out.write("Number of Phrases: {0}\n\n".format(len(phrases)))

            out.write(rst_header("Time Signature", 3))
            time_signature = Counter([phrase.time_signature[0] for phrase in phrases])
            out.write(rst_table(_utils.percentage(time_signature)))
            out.write("\n\n")

            out.write(rst_header("Ambitus in semitones", 3))
            ambitus = Counter([phrase.ambitus for phrase in phrases])
            out.write(rst_table(_utils.percentage(ambitus)))
            out.write("\n\n")


    with codecs.open("doc/basic_data.rst", 'w', encoding="utf-8") as out:
        out.write(rst_header(u"Basic Data", 1))

        all_phrases = _utils.flatten(alist.values())
        print_data('All composers', all_phrases)

        for composer, phrases in sorted(alist.items()):
            print_data(composer, phrases)


if __name__ == '__main__':
    collection_dict = _utils.make_composer_dict('choros-corpus')
    make_basic_data_webpage(collection_dict)
