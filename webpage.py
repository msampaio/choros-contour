#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import os
from collections import Counter
import _utils
import data
import plot


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

        def aux(title, data, plot_fn):
            # plotting
            dest = os.path.join("doc/contour", composer.replace(" ", "-") + "-" + title.replace(" ", "-") + ".png")
            pngfile = os.path.splitext(os.path.basename(dest))[0]
            plot.clear()
            plot_fn(data.values(), data.keys(), None, dest)

            # print in rst
            out.write(rst_header(title, 3))
            out.write(rst_image(pngfile, "contour", 90))
            out.write(rst_table(_utils.percentage(data)))
            out.write("\n\n")

        print "Processing phrases of composer... {0}".format(composer)

        songs_number = _utils.count_songs_from_phrases(phrases)

        out.write(rst_header(composer, 2))

        out.write("Number of Songs: {0}\n\n".format(songs_number))
        out.write("Number of Phrases: {0}\n\n".format(len(phrases)))

        aux('Time signature', Counter([phrase.time_signature[0] for phrase in phrases]), plot.simple_pie)
        aux('Ambitus in semitones', Counter([phrase.ambitus for phrase in phrases]), plot.simple_scatter)

    with codecs.open("doc/basic_data.rst", 'w', encoding="utf-8") as out:
        out.write(rst_header(u"Basic Data", 1))
        out.write('This page contains basic data of choros phrases such as time signature organized by composer. ')
        out.write('The numbers in the table\'s second column are in percent.\n\n')

        all_phrases = _utils.flatten(alist.values())
        print_data('All composers', all_phrases)

        for composer, phrases in sorted(alist.items()):
            print_data(composer, phrases)


if __name__ == '__main__':
    collection_dict = _utils.make_composer_dict('choros-corpus')
    make_basic_data_webpage(collection_dict)
