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
import song
import query
import songcollections


class WebpageError(Exception):
    pass


def rst_header(title, level=1):
    """Return a string formatted for rst code header."""

    levels = u"* = - ^".split()

    if level > 4 or level < 1:
        raise WebpageError("We have levels from 1 to 4")

    header = levels[level - 1] * len(title)
    return u"{0}\n{1}\n\n".format(title, header)


def rst_image(filename, directory, scale_factor=100):
    """Return a string formatted for rst code figure."""

    return u".. image:: {0}/{1}.png\n   :scale: {2}\n".format(directory, filename, scale_factor)


def rst_table(dic, size=8):
    """Return a string formatted for rst code table. The input data is
    a dictionary such as {'a': 2, 'b': 4, 'c': 6}."""

    mark = "{0} {0}".format("=" * size)
    result = [mark]
    for key, val in _utils.sort2(dic):
        result.append("{1:{0}} {2:{0}.2f}".format(size, key, val))
    result.append(mark)
    return "\n".join(result)


def print_plot(out, title, composer, data, plot_fn):
    """Write header, chart and table in a given codecs.open object
    with a given data of a given composer."""

    # plotting
    directory = "docs/contour"
    r_composer = composer.replace(" ", "-")
    r_title = title.replace(" ", "-")
    dest = _utils.unicode_normalize(os.path.join(directory, r_composer + "-" + r_title + ".png"))
    pngfile = os.path.splitext(os.path.basename(dest))[0]
    plot.clear()
    if plot_fn == plot.simple_scatter:
        plot_fn(data.values(), data.keys(), ['Percentual of segments (%)', title], None, dest)
    else:
        plot_fn(data.values(), data.keys(), None, dest)

    # print in rst
    out.write(rst_header(title, 3))
    out.write(rst_image(pngfile, "contour", 90))
    out.write(rst_table(_utils.percentage(data)))
    out.write("\n\n")


def print_basic_data(out, composer, AllSegmentsObj, allSegments_number):
    """Write data in a codecs.open object for basic_data page."""

    def count_segments(AllSegmentsObj, attrib):
        return Counter((getattr(seg, attrib) for seg in AllSegmentsObj.segments))

    print "Processing segments of composer... {0}".format(composer)

    songs_number = len(AllSegmentsObj.allFilenames)
    percentual_allSegments = AllSegmentsObj.segments_number / float(allSegments_number) * 100

    out.write(rst_header(composer, 2))

    out.write("Number of Songs: {0}\n\n".format(songs_number))
    if percentual_allSegments != 100:
        out.write("Percentual of all segments: {0:.2f}%\n\n".format(percentual_allSegments))
    out.write("Number of segments: {0}\n\n".format(AllSegmentsObj.segments_number))


    print_plot(out, 'Meter', composer, count_segments(AllSegmentsObj, 'meter'), plot.simple_pie)
    print_plot(out, 'Ambitus in semitones', composer, count_segments(AllSegmentsObj, 'ambitus'), plot.simple_scatter)
    print_plot(out, 'Pickup measure', composer, count_segments(AllSegmentsObj, 'pickup'), plot.simple_pie)


def make_basic_data_webpage(AllSegmentsObj):
    """Create and save data of basic_data webpage. The input data is
    an AllSegments object."""

    print "Creating basic data webpage..."

    with codecs.open("docs/basic_data.rst", 'w', encoding="utf-8") as out:
        out.write(rst_header(u"Basic Data", 1))
        out.write('This page contains basic data of choros segments such as time signature organized by composer. ')
        out.write('The numbers in the table\'s second column are in percent.\n\n')

        print_basic_data(out, 'All composers', AllSegmentsObj, AllSegmentsObj.segments_number)

        for composer in AllSegmentsObj.allComposers:
            segments = AllSegmentsObj.getByComposer(composer)
            print_basic_data(out, composer, segments, AllSegmentsObj.segments_number)


def print_contour(out, composer, AllSegmentsObj, allSegments_number):
    """Write data in a codecs.open object for contour page."""

    print "Processing segments of composer... {0}".format(composer)

    songs_number = len(AllSegmentsObj.allFilenames)
    percentual_allSegments = AllSegmentsObj.segments_number / float(allSegments_number) * 100

    out.write(rst_header(composer, 2))

    out.write("Number of Songs: {0}\n\n".format(songs_number))
    if percentual_allSegments != 100:
        out.write("Percentual of all segments: {0:.2f}%\n\n".format(percentual_allSegments))
    out.write("Number of Segments: {0}\n\n".format(AllSegmentsObj.segments_number))

    print_plot(out, 'Contour Prime', composer, _utils.group_minorities(contour.contour_prime_count(AllSegmentsObj.segments), 0.04), plot.simple_pie)
    print_plot(out, 'Highest Contour Point', composer, contour.contour_highest_cp_count(AllSegmentsObj.segments), plot.simple_scatter)
    print_plot(out, 'Passing contour', composer, contour.multicount(AllSegmentsObj.segments, contour.passing_contour), plot.simple_scatter)
    print_plot(out, 'Contour oscillation index', composer, contour.contour_oscillation_count(AllSegmentsObj.segments), plot.simple_scatter)
    print_plot(out, 'Contour first movement', composer, contour.first_movement(AllSegmentsObj.segments), plot.simple_pie)
    print_plot(out, 'Contour last movement', composer, contour.last_movement(AllSegmentsObj.segments), plot.simple_pie)


def make_contour_webpage(AllSegmentsObj):
    """Create and save data of contour webpage. The input data is an
    AllSegments object."""

    print "Creating contour webpage..."

    with codecs.open("docs/contour.rst", 'w', encoding="utf-8") as out:
        out.write(rst_header(u"Contour", 1))
        out.write('This page contains contour data of choros segments such as Contour Primes organized by composer.\n\n')
        out.write('The explanation about the charts below are in `glossary <glossary.html>`_.\n\n')

        print_contour(out, 'All composers', AllSegmentsObj, AllSegmentsObj.segments_number)

        for composer in AllSegmentsObj.allComposers:
            segments = AllSegmentsObj.getByComposer(composer)
            print_contour(out, composer, segments, AllSegmentsObj.segments_number)


def make_corpus_webpage(songsList, collectionsObj):
    """Create and save data of corpus webpage. The input data is a
    list of Song objects and a SongCollections object."""

    print "Creating corpus webpage..."

    with codecs.open("docs/corpus.rst", 'w', encoding="utf-8") as out:
        out.write(rst_header(u"Corpus information", 1))
        out.write('This page contains information about analyzed corpus such as composers and song names.\n\n')

        total_songs = collectionsObj.number
        processed_songs = len(songsList)
        percentual_songs = processed_songs / float(total_songs) * 100
        date = datetime.datetime.today().date().isoformat()

        out.write('Processed songs: {0} of {1} ({2:.2f}%) until {3}.\n\n'.format(processed_songs, total_songs, percentual_songs, date))

        out.write(rst_header('Composers', 2))
        composers_dic = {}
        for s in songsList:
            composer = s.composer
            if composer not in composers_dic:
                composers_dic[composer] = 0
            composers_dic[composer] += 1
        n = 0
        for composer, songs in sorted(composers_dic.items()):
            if songs > 1:
                plural = 's'
            else:
                plural = ''
            out.write('{0}. {1} ({2} song{3})\n\n'.format(n + 1, composer, songs, plural))
            n += 1

        out.write(rst_header('Songs', 2))
        for n, s in enumerate(sorted(songsList, key=lambda x: x.title)):
            out.write('{0}. {1} ({2})\n\n'.format(n + 1, s.title, s.composer))


def make_collections_webpage(collectionsObj):
    """Create and save data of collections webpage. The input data is
    an AllSegments object."""

    print "Creating collections webpage..."

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


def print_lily(out, SegmentObj, subtitle):
    """Write data in a codecs.open object for special_cases page,
    including lilypond file generation."""

    # plotting
    directory = "docs/contour"
    r_composer = SegmentObj.composer.replace(" ", "-")
    r_title = SegmentObj.title.replace(" ", "-")
    r_typeof = SegmentObj.typeof
    r_number = str(SegmentObj.number)
    filename = "-".join([r_composer, r_title, r_typeof, r_number])
    dest = _utils.unicode_normalize(os.path.join(directory, filename +  ".png"))
    pngfile = os.path.splitext(os.path.basename(dest))[0]
    SegmentObj.make_score()
    SegmentObj.score.write('png', dest)
    _utils.image_trim(dest)

    title = ", ".join([SegmentObj.title, SegmentObj.composer, " ".join([SegmentObj.typeof, str(SegmentObj.number)]), subtitle])
    # print in rst
    out.write(rst_header(title, 4))
    out.write(rst_image(pngfile, "contour", 90))
    out.write("\n\n")


def make_special_cases_webpage(AllSegmentsObj, songsObj):
    """Create and save data of special_cases webpage. The input data
    is an AllSegments object."""

    print "Creating special cases webpage..."

    with codecs.open("docs/special_cases.rst", 'w', encoding="utf-8") as out:
        out.write(rst_header(u"Special cases", 1))
        out.write('This page contains segments with data such as higher and lower ambitus.\n\n')

        # ambitus
        allAmbitus = AllSegmentsObj.allAmbitus
        higher_ambitus = max(allAmbitus)
        lower_ambitus = min(allAmbitus)

        higher_ambitus_segment = AllSegmentsObj.getByAmbitus(higher_ambitus).segments[0]
        lower_ambitus_segment = AllSegmentsObj.getByAmbitus(lower_ambitus).segments[0]

        out.write(rst_header('Ambitus', 2))
        out.write(rst_header('Higher', 3))
        print_lily(out, higher_ambitus_segment, '{0} semitones'.format(higher_ambitus))
        out.write(rst_header('Lower', 3))
        print_lily(out, lower_ambitus_segment, '{0} semitones'.format(lower_ambitus))

        # oscillation contour
        oscillation_list = []
        for SegmentObj in AllSegmentsObj.segments:
            oscillation_value = SegmentObj.contour.oscillation_index()
            oscillation_list.append((oscillation_value, SegmentObj))
        higher_oscillation = sorted(oscillation_list, key = lambda el: el[0], reverse=True)[0]
        lower_oscillation = sorted(oscillation_list, key = lambda el: el[0])[0]

        out.write(rst_header('Contour oscillation index', 2))
        out.write(rst_header('Most oscillated', 3))
        print_lily(out, higher_oscillation[1], '{0} (from 0 to 1)'.format(round(higher_oscillation[0], 2)))
        out.write(rst_header('Least oscillated', 3))
        print_lily(out, lower_oscillation[1], '{0} (from 0 to 1)'.format(round(lower_oscillation[0], 2)))

        # period similarity
        periods = song.makeStructuresList(songsObj)
        comparison_list = contour.period_comparison(periods)
        acmemb_values = [x[1] for x in comparison_list]

        higher_similarity = sorted(comparison_list, key = lambda el: el[1], reverse=True)[0]
        lower_similarity = sorted(comparison_list, key = lambda el: el[1])[0]

        print higher_similarity[0][0]
        out.write(rst_header('Prime contour similarity index', 2))
        out.write(rst_header('Most similar', 3))
        print_lily(out, higher_similarity[0][0], '{0} (from 0 to 1)'.format(round(higher_similarity[1], 2)))
        print_lily(out, higher_similarity[0][1], '{0} (from 0 to 1)'.format(round(higher_similarity[1], 2)))
        out.write(rst_header('Least similar', 3))
        print_lily(out, lower_similarity[0][0], '{0} (from 0 to 1)'.format(round(lower_similarity[1], 2)))
        print_lily(out, lower_similarity[0][1], '{0} (from 0 to 1)'.format(round(lower_similarity[1], 2)))


def print_period(out, composer, ComposerSongObjList, number_of_periods):
    """Write data in a codecs.open object for contour page."""

    print "Processing segments of composer... {0}".format(composer)

    periods = song.makeStructuresList(ComposerSongObjList)
    comparison_list = contour.period_comparison(periods)
    acmemb_values = [x[1] for x in comparison_list]

    n = len(periods)
    percentual_allPeriods = n * 100 / float(number_of_periods)

    out.write(rst_header(composer, 2))
    if percentual_allPeriods != 100:
        out.write("Percentual of all periods: {0:.2f}%\n\n".format(percentual_allPeriods))
    out.write("Number of periods: {0}\n\n".format(n))

    print_plot(out, 'All Mutually Embedded Contour', composer, Counter(acmemb_values), plot.simple_scatter)


def make_periods_webpage(songsObj):
    """Create and save data of periods webpage. The input data is a
    list of Song objects."""

    print "Creating periods webpage..."

    with codecs.open("docs/periods.rst", 'w', encoding="utf-8") as out:
        out.write(rst_header(u"Periods", 1))
        out.write('This page contains data of choros periods such as contour similarity organized by composer.\n\n')

        number_of_periods = len(song.makeStructuresList(songsObj))

        print_period(out, 'All composers', songsObj, number_of_periods)

        composers_dic = {}
        for songObj in songsObj:
            composer = songObj.composer
            if composer not in composers_dic:
                composers_dic[composer] = []
            composers_dic[composer].append(songObj)

        for composer in sorted(composers_dic.keys()):
            print_period(out, composer, composers_dic[composer], number_of_periods)


def run():
    _utils.mkdir('docs/contour')
    songsObj = retrieval.loadSongs()
    AllSegmentsObj = retrieval.loadSegments()
    collectionsSeq = json.load(open('songs_map.json'))
    collectionsObj = songcollections.makeAllCollectionSongs(collectionsSeq)
    
    make_basic_data_webpage(AllSegmentsObj)
    make_contour_webpage(AllSegmentsObj)
    make_corpus_webpage(songsObj, collectionsObj)
    make_collections_webpage(collectionsObj)
    make_special_cases_webpage(AllSegmentsObj, songsObj)
    make_periods_webpage(songsObj)


if __name__ == '__main__':
    run()
