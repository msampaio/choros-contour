#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import os
from collections import Counter
import _utils
import data
import plot
import contour
import query


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


def print_plot(out, title, composer, data, plot_fn):
    # plotting
    directory = "docs/contour"
    r_composer = composer.replace(" ", "-")
    r_title = title.replace(" ", "-")
    dest = _utils.unicode_normalize(os.path.join(directory, r_composer + "-" + r_title + ".png"))
    pngfile = os.path.splitext(os.path.basename(dest))[0]
    plot.clear()
    if plot_fn == plot.simple_scatter:
        plot_fn(data.values(), data.keys(), ['Percentual of music units (%)', title], None, dest)
    else:
        plot_fn(data.values(), data.keys(), None, dest)

    # print in rst
    out.write(rst_header(title, 3))
    out.write(rst_image(pngfile, "contour", 90))
    out.write(rst_table(_utils.percentage(data)))
    out.write("\n\n")


def print_basic_data(out, composer, unitObj, allUnits_number):

    def count_units(unitObj, attrib):
        return Counter((getattr(u, attrib) for u in unitObj.units))

    print "Processing units of composer... {0}".format(composer)

    songs_number = len(unitObj.allFilenames)
    percentual_allUnits = unitObj.units_number / float(allUnits_number) * 100

    out.write(rst_header(composer, 2))

    out.write("Number of Songs: {0}\n\n".format(songs_number))
    if percentual_allUnits != 100:
        out.write("Percentual of all units: {0:.2f}%\n\n".format(percentual_allUnits))
    out.write("Number of Units: {0}\n\n".format(unitObj.units_number))


    print_plot(out, 'Meter', composer, count_units(unitObj, 'meter'), plot.simple_pie)
    print_plot(out, 'Ambitus in semitones', composer, count_units(unitObj, 'ambitus'), plot.simple_scatter)
    print_plot(out, 'Pickup measure', composer, count_units(unitObj, 'pickup'), plot.simple_pie)


def make_basic_data_webpage(unitObj):

    with codecs.open("docs/basic_data.rst", 'w', encoding="utf-8") as out:
        out.write(rst_header(u"Basic Data", 1))
        out.write('This page contains basic data of choros music units such as time signature organized by composer. ')
        out.write('The numbers in the table\'s second column are in percent.\n\n')

        print_basic_data(out, 'All composers', unitObj, unitObj.units_number)

        for composer in unitObj.allComposers:
            subunits = unitObj.getByComposer(composer)
            print_basic_data(out, composer, subunits, unitObj.units_number)


def print_contour(out, composer, unitObj, allUnits_number):

    print "Processing units of composer... {0}".format(composer)

    songs_number = len(unitObj.allFilenames)
    percentual_allUnits = unitObj.units_number / float(allUnits_number) * 100

    out.write(rst_header(composer, 2))

    out.write("Number of Songs: {0}\n\n".format(songs_number))
    if percentual_allUnits != 100:
        out.write("Percentual of all units: {0:.2f}%\n\n".format(percentual_allUnits))
    out.write("Number of Units: {0}\n\n".format(unitObj.units_number))

    print_plot(out, 'Contour Prime', composer, _utils.group_minorities(contour.contour_prime_count(unitObj.units), 0.04), plot.simple_pie)
    print_plot(out, 'Highest Contour Point', composer, contour.contour_highest_cp_count(unitObj.units), plot.simple_scatter)
    print_plot(out, 'Passing contour', composer, contour.passing_contour(unitObj.units), plot.simple_scatter)


def make_contour_webpage(unitObj):

    with codecs.open("docs/contour.rst", 'w', encoding="utf-8") as out:
        out.write(rst_header(u"Contour", 1))
        out.write('This page contains contour data of choros music units such as Contour Primes organized by composer. ')
        out.write('Highest contour points means the number of different contour points. ')
        out.write('A great value of passing contour incidence means that a music unit has many successive cp in the same direction. ')
        out.write('The numbers in the table\'s second column are in percent.\n\n')

        print_contour(out, 'All composers', unitObj, unitObj.units_number)

        for composer in unitObj.allComposers:
            subunits = unitObj.getByComposer(composer)
            print_contour(out, composer, subunits, unitObj.units_number)


def run():
    _utils.mkdir('docs/contour')
    unitObj = data.loadMusicUnits()
    make_basic_data_webpage(unitObj)
    make_contour_webpage(unitObj)


if __name__ == '__main__':
    run()
