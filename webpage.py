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


# review
def make_basic_data_webpage(alist):

    def print_attribute(attribute, collection, out):
        counter = Counter([getattr(song, attribute) for song in collection])
        out.write(rst_table(_utils.percentage(counter)))
        out.write("\n\n")

    with codecs.open("doc/basic_data.rst", 'w', encoding="utf-8") as out:
        out.write(rst_header(u"Basic Data", 1))

        for name, collection in alist.items():
            print "Processing collection... {0}".format(name)

            collection_phrases = _utils.flatten(collection)

            out.write(rst_header(name, 2))

            out.write("Number of Songs: {0}\n\n".format(len(collection)))
            out.write("Number of Phrases: {0}\n\n".format(len(collection_phrases)))

            out.write(rst_header("Time Signature", 3))
            time_signature = Counter([phrase.time_signature[0] for phrase in collection_phrases])
            out.write(rst_table(_utils.percentage(time_signature)))
            out.write("\n\n")

            out.write(rst_header("Ambitus in semitones", 3))
            ambitus = Counter([phrase.ambitus for phrase in collection_phrases])
            out.write(rst_table(_utils.percentage(ambitus)))
            out.write("\n\n")


if __name__ == '__main__':
    PIXINGUINHA = data.load_pickle("pixinguinha")

    make_basic_data_webpage({
        "O Melhor de Pixinguinha": PIXINGUINHA,
        })
