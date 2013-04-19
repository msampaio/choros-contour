#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import os
from collections import Counter
import json
import datetime
import _utils
import retrieval
import plot
import contour
import query
import songcollections


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


def print_basic_data(out, composer, AllMusicUnitsObj, allUnits_number):

    def count_units(AllMusicUnitsObj, attrib):
        return Counter((getattr(un, attrib) for un in AllMusicUnitsObj.units))

    print "Processing music units of composer... {0}".format(composer)

    songs_number = len(AllMusicUnitsObj.allFilenames)
    percentual_allUnits = AllMusicUnitsObj.units_number / float(allUnits_number) * 100

    out.write(rst_header(composer, 2))

    out.write("Number of Songs: {0}\n\n".format(songs_number))
    if percentual_allUnits != 100:
        out.write("Percentual of all music units: {0:.2f}%\n\n".format(percentual_allUnits))
    out.write("Number of music units: {0}\n\n".format(AllMusicUnitsObj.units_number))


    print_plot(out, 'Meter', composer, count_units(AllMusicUnitsObj, 'meter'), plot.simple_pie)
    print_plot(out, 'Ambitus in semitones', composer, count_units(AllMusicUnitsObj, 'ambitus'), plot.simple_scatter)
    print_plot(out, 'Pickup measure', composer, count_units(AllMusicUnitsObj, 'pickup'), plot.simple_pie)


def make_basic_data_webpage(AllMusicUnitsObj):

    with codecs.open("docs/basic_data.rst", 'w', encoding="utf-8") as out:
        out.write(rst_header(u"Basic Data", 1))
        out.write('This page contains basic data of choros music units such as time signature organized by composer. ')
        out.write('The numbers in the table\'s second column are in percent.\n\n')

        print_basic_data(out, 'All composers', AllMusicUnitsObj, AllMusicUnitsObj.units_number)

        for composer in AllMusicUnitsObj.allComposers:
            subunits = AllMusicUnitsObj.getByComposer(composer)
            print_basic_data(out, composer, subunits, AllMusicUnitsObj.units_number)


def print_contour(out, composer, AllMusicUnitsObj, allUnits_number):

    print "Processing units of composer... {0}".format(composer)

    songs_number = len(AllMusicUnitsObj.allFilenames)
    percentual_allUnits = AllMusicUnitsObj.units_number / float(allUnits_number) * 100

    out.write(rst_header(composer, 2))

    out.write("Number of Songs: {0}\n\n".format(songs_number))
    if percentual_allUnits != 100:
        out.write("Percentual of all units: {0:.2f}%\n\n".format(percentual_allUnits))
    out.write("Number of Units: {0}\n\n".format(AllMusicUnitsObj.units_number))

    print_plot(out, 'Contour Prime', composer, _utils.group_minorities(contour.contour_prime_count(AllMusicUnitsObj.units), 0.04), plot.simple_pie)
    print_plot(out, 'Highest Contour Point', composer, contour.contour_highest_cp_count(AllMusicUnitsObj.units), plot.simple_scatter)
    print_plot(out, 'Passing contour', composer, contour.multicount(AllMusicUnitsObj.units, contour.passing_contour), plot.simple_scatter)
    print_plot(out, 'Contour oscillation index', composer, contour.contour_oscillation_count(AllMusicUnitsObj.units), plot.simple_scatter)


def make_contour_webpage(AllMusicUnitsObj):

    with codecs.open("docs/contour.rst", 'w', encoding="utf-8") as out:
        out.write(rst_header(u"Contour", 1))
        out.write('This page contains contour data of choros music units such as Contour Primes organized by composer. ')
        out.write('Highest contour points means the number of different contour points. ')
        out.write('A great value of passing contour incidence means that a music unit has many successive cp in the same direction. ')
        out.write('The numbers in the table\'s second column are in percent.\n\n')

        print_contour(out, 'All composers', AllMusicUnitsObj, AllMusicUnitsObj.units_number)

        for composer in AllMusicUnitsObj.allComposers:
            subunits = AllMusicUnitsObj.getByComposer(composer)
            print_contour(out, composer, subunits, AllMusicUnitsObj.units_number)


def make_corpus_webpage(songsObj, collectionsObj):

    with codecs.open("docs/corpus.rst", 'w', encoding="utf-8") as out:
        out.write(rst_header(u"Corpus information", 1))
        out.write('This page contains information about analyzed corpus such as composers and song names.\n\n')

        total_songs = collectionsObj.number
        processed_songs = len(songsObj)
        percentual_songs = processed_songs / float(total_songs) * 100
        date = datetime.datetime.today().date().isoformat()

        out.write('Processed songs: {0} of {1} ({2:.2f}%) until {3}.\n\n'.format(processed_songs, total_songs, percentual_songs, date))

        out.write(rst_header('Composers', 2))
        for n, s in enumerate(songsObj):
            out.write('{0}. {1}\n\n'.format(n + 1, s.composer))

        out.write(rst_header('Songs', 2))
        for n, s in enumerate(songsObj):
            out.write('{0}. {1} ({2})\n\n'.format(n + 1, s.title, s.composer))


def make_collections_webpage(collectionsObj):

    with codecs.open("docs/collections.rst", 'w', encoding="utf-8") as out:
        out.write(rst_header(u"Collections information", 1))
        out.write('This page contains information about all collections to be analysed such as composers and song names.\n\n')

        out.write(rst_header('Collections', 2))
        for n, collection in enumerate(collectionsObj.allCollections):
            out.write('{0}. {1}\n\n'.format(n + 1, collection))

        out.write(rst_header('Composers', 2))
        for n, composer in enumerate(collectionsObj.allComposers):
            out.write('{0}. {1}\n\n'.format(n + 1, composer))

        # FIXME: use table instead of list
        out.write(rst_header('Songs', 2))
        for n, collObj in enumerate(sorted(collectionsObj.collectionSongs, key=lambda coll: coll.title)):
            out.write('{0}. {1} ({2}) - {3}\n\n'.format(n + 1, collObj.title, collObj.composer, collObj.collection))


def print_lily(out, MusicUnitObj, subtitle):
    # plotting
    directory = "docs/contour"
    r_composer = MusicUnitObj.composer.replace(" ", "-")
    r_title = MusicUnitObj.title.replace(" ", "-")
    r_typeof = MusicUnitObj.typeof
    r_number = str(MusicUnitObj.number)
    filename = "-".join([r_composer, r_title, r_typeof, r_number])
    dest = _utils.unicode_normalize(os.path.join(directory, filename +  ".png"))
    pngfile = os.path.splitext(os.path.basename(dest))[0]
    MusicUnitObj.make_score()
    MusicUnitObj.score.write('png', dest)
    _utils.trim(dest)

    title = ", ".join([MusicUnitObj.title, MusicUnitObj.composer, " ".join([MusicUnitObj.typeof, str(MusicUnitObj.number)]), subtitle])
    # print in rst
    out.write(rst_header(title, 4))
    out.write(rst_image(pngfile, "contour", 90))
    out.write("\n\n")


def make_special_cases_webpage(AllMusicUnitsObj):

    with codecs.open("docs/special_cases.rst", 'w', encoding="utf-8") as out:
        out.write(rst_header(u"Special cases", 1))
        out.write('This page contains music units with data such as higher and lower ambitus.\n\n')

        # ambitus
        allAmbitus = AllMusicUnitsObj.allAmbitus
        higher_ambitus = max(allAmbitus)
        lower_ambitus = min(allAmbitus)

        higher_ambitus_unit = AllMusicUnitsObj.getByAmbitus(higher_ambitus).units[0]
        lower_ambitus_unit = AllMusicUnitsObj.getByAmbitus(lower_ambitus).units[0]

        out.write(rst_header('Higher ambitus', 3))
        print_lily(out, higher_ambitus_unit, '{0} semitones'.format(higher_ambitus))
        out.write(rst_header('Lower ambitus', 3))
        print_lily(out, lower_ambitus_unit, '{0} semitones'.format(lower_ambitus))

        # oscillation contour
        oscillation_list = []
        for MusicUnitObj in AllMusicUnitsObj.units:
            oscillation_value = MusicUnitObj.contour.oscillation_index()
            oscillation_list.append((oscillation_value, MusicUnitObj))
        higher_oscillation = sorted(oscillation_list, key = lambda el: el[0], reverse=True)[0]
        lower_oscillation = sorted(oscillation_list, key = lambda el: el[0])[0]

        out.write(rst_header('Most oscillated contour', 3))
        print_lily(out, higher_oscillation[1], '{0} %'.format(round(higher_oscillation[0], 2)))
        out.write(rst_header('Less oscillated contour', 3))
        print_lily(out, lower_oscillation[1], '{0} %'.format(round(lower_oscillation[0], 2)))


def run():
    _utils.mkdir('docs/contour')
    songsObj = retrieval.loadSongs()
    AllMusicUnitsObj = retrieval.loadMusicUnits()
    collectionsSeq = json.load(open('songs_map.json'))
    collectionsObj = songcollections.makeAllCollectionSongs(collectionsSeq)
    
    make_basic_data_webpage(AllMusicUnitsObj)
    make_contour_webpage(AllMusicUnitsObj)
    make_corpus_webpage(songsObj, collectionsObj)
    make_collections_webpage(collectionsObj)
    make_special_cases_webpage(AllMusicUnitsObj)


if __name__ == '__main__':
    run()
