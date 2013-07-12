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
import intervals
import matrix
import questions


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

    return u".. image:: {0}/{1}.png\n   :scale: {2}\n\n".format(directory, filename, scale_factor)


def rst_table(dic):
    """Return a string formatted for rst code table. The input data is
    a dictionary such as {'a': 2, 'b': 4, 'c': 6}."""

    table_data = _utils.sort2(dic)
    larger_value = max([len(str(el)) for el in _utils.flatten(table_data)])

    mark = "{0}    {0}".format("=" * (larger_value))
    result = [mark]
    for key, val in table_data:
        result.append("{1:{0}} {2:{0}.2f}".format(larger_value, key, val))
    result.append(mark)
    return "\n".join(result)


def rst_link(link):
    """Return a string formatted for rst code link. The input is a
    link path."""

    return ":download:`MIDI <{0}>`".format(link)


def rst_plot(out, title, pngfile, hierarchy=3, size=90, midifile=None):
    """Return a string formatted for rst code plot. With optional
    given data, the function writes a also a table in rst."""

    out.write(rst_header(title, hierarchy))
    out.write(rst_image(pngfile, "contour", size))
    if midifile:
        out.write(rst_link(midifile))
    out.write("\n\n")


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
            composers = s.composers
            for composer in composers:
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
            out.write('{0}. {1} ({2})\n\n'.format(n + 1, s.title, s.composersStr))


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
            out.write('{0}. {1} ({2}) - {3}\n\n'.format(n + 1, collObj.title, collObj.composersStr, collObj.collection))


def makePlot(plotDic):
    """Write header, chart and table in a given codecs.open object
    with a given data of a given composer."""

    title = plotDic['title']
    topComposers = plotDic['topComposers']
    AllSegmentsObj = plotDic['AllSegmentsObj']
    plotFn = plotDic['plotFn']
    dest = plotDic['dest']

    # plot
    plot.clear()
    if plotFn == plot.attribStackedBarSave:
        attrib = plotDic['attrib']
        valuesNumber = plotDic['valuesNumber']
        plot.attribStackedBarSave(AllSegmentsObj, attrib, topComposers, valuesNumber, title, 'Segments (%)', dest)
    elif plotFn == plot.multipleScatterSave:
        attrib = plotDic['attrib']
        coordSequence = plotDic['coordSequence']
        legend = plotDic['legend']
        labels = plotDic['labels']
        plot.multipleScatterSave(coordSequence, legend, labels, title, dest)
    elif plotFn == plot.dataStackedBarSave:
        dataMatrix = plotDic['matrix']
        plot.dataStackedBarSave(dataMatrix, title, 'Segments (%)', dest)


def plot_print_rst(plotDic):
    # files data
    out = plotDic['out']
    title = plotDic['title']

    hierarchy = _utils.dicValueInsertion(plotDic, 'hierarchy', 3)
    size = _utils.dicValueInsertion(plotDic, 'size', 90)

    directory = "docs/contour"
    r_title = title.replace(" ", "-")
    dest = _utils.unicode_normalize(os.path.join(directory, r_title + ".png"))
    pngfile = os.path.splitext(os.path.basename(dest))[0]

    # plot
    plotDic['dest'] = dest
    makePlot(plotDic)

    # print in rst
    rst_plot(out, title, pngfile, hierarchy, size)

def makeMeterChart(out, AllSegmentsObj, topComposers, valuesNumber=3):
    # meter (bar)
    print '. Creating meter chart...'

    meterDic = {}
    meterDic['plotFn'] = plot.attribStackedBarSave
    meterDic['out'] = out
    meterDic['attrib'] = 'meter'
    meterDic['title'] = 'Meter'
    meterDic['AllSegmentsObj'] = AllSegmentsObj
    meterDic['topComposers'] = topComposers
    meterDic['valuesNumber'] = valuesNumber
    meterDic['size'] = 100
    plot_print_rst(meterDic)


def makePickupChart(out, AllSegmentsObj, topComposers, valuesNumber=2):
    # pickup (bar)
    print '. Creating pickup chart...'

    pickupDic = {}
    pickupDic['plotFn'] = plot.attribStackedBarSave
    pickupDic['out'] = out
    pickupDic['attrib'] = 'pickup'
    pickupDic['title'] = 'Pickup'
    pickupDic['AllSegmentsObj'] = AllSegmentsObj
    pickupDic['topComposers'] = topComposers
    pickupDic['valuesNumber'] = valuesNumber
    pickupDic['size'] = 100
    plot_print_rst(pickupDic)


def makeMeasuresNChart(out, AllSegmentsObj, topComposers, valuesNumber=6):
    # measuresN (bar)
    print '. Creating measuresN chart...'

    measuresNDic = {}
    measuresNDic['plotFn'] = plot.attribStackedBarSave
    measuresNDic['out'] = out
    measuresNDic['attrib'] = 'measuresNumber'
    measuresNDic['title'] = 'Number of measures'
    measuresNDic['AllSegmentsObj'] = AllSegmentsObj
    measuresNDic['topComposers'] = topComposers
    measuresNDic['valuesNumber'] = valuesNumber
    measuresNDic['size'] = 100
    plot_print_rst(measuresNDic)


def makeTotalLengthChart(out, AllSegmentsObj, topComposers, AllAndTopComposers):
    # TotalLength (bar)
    print '. Creating TotalLength chart...'

    totalLengthDic = {}
    totalLengthDic['plotFn'] = plot.multipleScatterSave
    totalLengthDic['out'] = out
    totalLengthDic['attrib'] = 'totalLength'
    totalLengthDic['title'] = 'Total Length'
    totalLengthDic['AllSegmentsObj'] = AllSegmentsObj
    totalLengthDic['topComposers'] = topComposers
    totalLengthDic['size'] = 100

    totalLengthDic['coordSequence'] = _utils.makeAttribCoordSequence(AllSegmentsObj, 'totalLength', topComposers)
    totalLengthDic['legend'] = ['Segments (%)', 'Length (in quarter values)']
    totalLengthDic['labels'] = AllAndTopComposers

    plot_print_rst(totalLengthDic)


def makeDurationsChart(out, AllSegmentsObj, topComposers, AllAndTopComposers, valuesNumber=5):
    # durations (bar)
    print '. Creating durations chart...'


    durationsDic = {}
    durationsDic['plotFn'] = plot.dataStackedBarSave
    durationsDic['out'] = out
    durationsDic['attrib'] = 'durations'
    durationsDic['title'] = 'Durations'
    durationsDic['valuesNumber'] = valuesNumber
    durationsDic['AllSegmentsObj'] = AllSegmentsObj
    durationsDic['topComposers'] = topComposers
    durationsDic['size'] = 100
    durationsDic['matrix'] = matrix.dataValuesMatrix(AllSegmentsObj, AllAndTopComposers, questions.allDurations, durationsDic['valuesNumber'])

    plot_print_rst(durationsDic)


def make_duration_webpage(AllSegmentsObj, topComposers):
    """Create and save data of Duration webpage. The input data is
    an AllSegments object and topComposers sequence."""

    print "Creating duration webpage..."

    with codecs.open("docs/duration.rst", 'w', encoding="utf-8") as out:
        out.write(rst_header(u"Duration", 1))
        out.write('This page contains basic data of Duration domain of choros segments such as meter.\n\n')

        AllAndTopComposers = _utils.flatten([['All composers'], topComposers])

        makeMeterChart(out, AllSegmentsObj, topComposers)
        makePickupChart(out, AllSegmentsObj, topComposers)
        makeMeasuresNChart(out, AllSegmentsObj, topComposers)
        makeTotalLengthChart(out, AllSegmentsObj, topComposers, AllAndTopComposers)
        makeDurationsChart(out, AllSegmentsObj, topComposers, AllAndTopComposers)


def makeAmbitusChart(out, AllSegmentsObj, topComposers, AllAndTopComposers):
    # ambitus (scatter)
    print '. Creating ambitus chart...'

    ambitusDic = {}
    ambitusDic['plotFn'] = plot.multipleScatterSave
    ambitusDic['out'] = out
    ambitusDic['attrib'] = 'ambitus'
    ambitusDic['title'] = 'Ambitus'
    ambitusDic['AllSegmentsObj'] = AllSegmentsObj
    ambitusDic['topComposers'] = topComposers
    ambitusDic['size'] = 100

    ambitusDic['coordSequence'] = _utils.makeAttribCoordSequence(AllSegmentsObj, 'ambitus', topComposers)
    ambitusDic['legend'] = ['Segments (%)', 'Semitones']
    ambitusDic['labels'] = AllAndTopComposers

    plot_print_rst(ambitusDic)


def makeConsonanceChart(out, AllSegmentsObj, topComposers, AllAndTopComposers, valuesNumber=2):
    # consonance (bar)
    print '. Creating consonance chart...'

    consonanceDic = {}
    consonanceDic['plotFn'] = plot.dataStackedBarSave
    consonanceDic['out'] = out
    consonanceDic['valuesNumber'] = valuesNumber
    consonanceDic['matrix'] = matrix.dataValuesMatrix(AllSegmentsObj, AllAndTopComposers, questions.consonance, consonanceDic['valuesNumber'])
    consonanceDic['title'] = 'Consonance'
    consonanceDic['AllSegmentsObj'] = AllSegmentsObj
    consonanceDic['topComposers'] = topComposers
    consonanceDic['size'] = 100

    plot_print_rst(consonanceDic)


def makeIntervalChart(out, AllSegmentsObj, topComposers, AllAndTopComposers, valuesNumber=8):
    # intervals (bar)
    print '. Creating intervals chart...'

    intervalDic = {}
    intervalDic['plotFn'] = plot.dataStackedBarSave
    intervalDic['out'] = out
    intervalDic['valuesNumber'] = valuesNumber
    intervalDic['matrix'] = matrix.dataValuesMatrix(AllSegmentsObj, AllAndTopComposers, questions.allIntervals, intervalDic['valuesNumber'])
    intervalDic['title'] = 'Intervals'
    intervalDic['AllSegmentsObj'] = AllSegmentsObj
    intervalDic['topComposers'] = topComposers
    intervalDic['size'] = 100

    plot_print_rst(intervalDic)


def makeIntervalSTChart(out, AllSegmentsObj, topComposers, AllAndTopComposers):
    # intervals in semitones (scatter)
    print '. Creating intervals in semitones chart...'

    intervalSTDic = {}
    intervalSTDic['plotFn'] = plot.multipleScatterSave
    intervalSTDic['out'] = out
    intervalSTDic['attrib'] = 'intervals_with_direction_semitones'
    intervalSTDic['title'] = 'Intervals in semitones'
    intervalSTDic['AllSegmentsObj'] = AllSegmentsObj
    intervalSTDic['topComposers'] = topComposers
    intervalSTDic['size'] = 100

    intervalSTDic['coordSequence'] = [_utils.makeDataCoordSequence(questions.allIntervalsST(AllSegmentsObj, composer)) for composer in AllAndTopComposers]
    intervalSTDic['legend'] = ['Segments (%)', 'Semitones']
    intervalSTDic['labels'] = AllAndTopComposers

    plot_print_rst(intervalSTDic)


def makeLeapsChart(out, AllSegmentsObj, topComposers, AllAndTopComposers, valuesNumber=8):
    # leaps (bar)
    print '. Creating leaps chart...'

    leapsDic = {}
    leapsDic['plotFn'] = plot.dataStackedBarSave
    leapsDic['out'] = out
    leapsDic['valuesNumber'] = valuesNumber
    leapsDic['matrix'] = matrix.dataValuesMatrix(AllSegmentsObj, AllAndTopComposers, questions.allLeaps, leapsDic['valuesNumber'])
    leapsDic['title'] = 'Leaps'
    leapsDic['AllSegmentsObj'] = AllSegmentsObj
    leapsDic['topComposers'] = topComposers
    leapsDic['size'] = 100

    plot_print_rst(leapsDic)


def makeStepsLeapsChart(out, AllSegmentsObj, topComposers, AllAndTopComposers, valuesNumber=4):
    # steps, leaps, 3rds, repetition (bar)
    print '. Creating steps, leaps and arpeggios chart...'

    stepsLeapsDic = {}
    stepsLeapsDic['plotFn'] = plot.dataStackedBarSave
    stepsLeapsDic['out'] = out
    stepsLeapsDic['valuesNumber'] = valuesNumber
    stepsLeapsDic['matrix'] = matrix.dataValuesMatrix(AllSegmentsObj, AllAndTopComposers, questions.stepLeapArpeggio, stepsLeapsDic['valuesNumber'])
    stepsLeapsDic['title'] = 'Steps, Leaps and Arpeggios'
    stepsLeapsDic['AllSegmentsObj'] = AllSegmentsObj
    stepsLeapsDic['topComposers'] = topComposers
    stepsLeapsDic['size'] = 100

    plot_print_rst(stepsLeapsDic)


def makeFirstMovementChart(out, AllSegmentsObj, topComposers, AllAndTopComposers, valuesNumber=2):
    # first movement (bar)
    print '. Creating first movement chart...'

    firstMovementDic = {}
    firstMovementDic['plotFn'] = plot.dataStackedBarSave
    firstMovementDic['out'] = out
    firstMovementDic['valuesNumber'] = valuesNumber
    firstMovementDic['matrix'] = matrix.dataValuesMatrix(AllSegmentsObj, AllAndTopComposers, questions.firstMovement, firstMovementDic['valuesNumber'])
    firstMovementDic['title'] = 'First movement'
    firstMovementDic['AllSegmentsObj'] = AllSegmentsObj
    firstMovementDic['topComposers'] = topComposers
    firstMovementDic['size'] = 100

    plot_print_rst(firstMovementDic)

def makeLastMovementChart(out, AllSegmentsObj, topComposers, AllAndTopComposers, valuesNumber=2):
    # last movement (bar)
    print '. Creating last movement chart...'

    lastMovementDic = {}
    lastMovementDic['plotFn'] = plot.dataStackedBarSave
    lastMovementDic['out'] = out
    lastMovementDic['valuesNumber'] = valuesNumber
    lastMovementDic['matrix'] = matrix.dataValuesMatrix(AllSegmentsObj, AllAndTopComposers, questions.lastMovement, lastMovementDic['valuesNumber'])
    lastMovementDic['title'] = 'Last movement'
    lastMovementDic['AllSegmentsObj'] = AllSegmentsObj
    lastMovementDic['topComposers'] = topComposers
    lastMovementDic['size'] = 100

    plot_print_rst(lastMovementDic)

def makeContourPrimeChart(out, AllSegmentsObj, topComposers, AllAndTopComposers, valuesNumber=5):
    # contour prime (bar)
    print '. Creating prime contour chart...'

    primeContourDic = {}
    primeContourDic['plotFn'] = plot.attribStackedBarSave
    primeContourDic['out'] = out
    primeContourDic['attrib'] = 'contour_prime'
    primeContourDic['title'] = 'Prime Contour'
    primeContourDic['AllSegmentsObj'] = AllSegmentsObj
    primeContourDic['topComposers'] = topComposers
    primeContourDic['valuesNumber'] = valuesNumber
    primeContourDic['size'] = 100

    plot_print_rst(primeContourDic)

def makeDifferentPointsChart(out, AllSegmentsObj, topComposers, AllAndTopComposers, valuesNumber=2):
    # DifferentPoints index (scatter)
    print '. Creating different Contour points chart...'

    differentPointsDic = {}
    differentPointsDic['plotFn'] = plot.multipleScatterSave
    differentPointsDic['out'] = out
    differentPointsDic['attrib'] = 'differentPoints'
    differentPointsDic['title'] = 'Different Contour Points'
    differentPointsDic['AllSegmentsObj'] = AllSegmentsObj
    differentPointsDic['topComposers'] = topComposers
    differentPointsDic['size'] = 100

    differentPointsDic['coordSequence'] = [_utils.makeDataCoordSequence(questions.differentPoints(AllSegmentsObj, composer)) for composer in AllAndTopComposers]
    differentPointsDic['legend'] = ['Segments (%)', 'Number of Contour Points']
    differentPointsDic['labels'] = AllAndTopComposers

    plot_print_rst(differentPointsDic)

def makeOscillationChart(out, AllSegmentsObj, topComposers, AllAndTopComposers, valuesNumber=2):
    # Oscillation index (scatter)
    print '. Creating oscillation index chart...'

    oscillationDic = {}
    oscillationDic['plotFn'] = plot.multipleScatterSave
    oscillationDic['out'] = out
    oscillationDic['attrib'] = 'oscillation'
    oscillationDic['title'] = 'Oscillation index'
    oscillationDic['AllSegmentsObj'] = AllSegmentsObj
    oscillationDic['topComposers'] = topComposers
    oscillationDic['size'] = 100

    oscillationDic['coordSequence'] = [_utils.makeDataCoordSequence(questions.oscillation(AllSegmentsObj, composer)) for composer in AllAndTopComposers]
    oscillationDic['legend'] = ['Segments (%)', 'Oscillation index']
    oscillationDic['labels'] = AllAndTopComposers

    plot_print_rst(oscillationDic)

def makeReductionBor355Chart(out, AllSegmentsObj, topComposers, AllAndTopComposers, valuesNumber=8):
    # first movement (bar)
    print '. Creating Reduction Bor 355 chart...'

    reductionBor355Dic = {}
    reductionBor355Dic['plotFn'] = plot.dataStackedBarSave
    reductionBor355Dic['out'] = out
    reductionBor355Dic['valuesNumber'] = valuesNumber
    reductionBor355Dic['matrix'] = matrix.dataValuesMatrix(AllSegmentsObj, AllAndTopComposers, questions.reductionBor355, reductionBor355Dic['valuesNumber'], True)
    reductionBor355Dic['title'] = 'Contour Reduction (Bor 355)'
    reductionBor355Dic['AllSegmentsObj'] = AllSegmentsObj
    reductionBor355Dic['topComposers'] = topComposers
    reductionBor355Dic['size'] = 100

    plot_print_rst(reductionBor355Dic)


def make_pitch_webpage(AllSegmentsObj, topComposers):
    """Create and save data of pitch webpage. The input data is
    an AllSegments object and topComposers sequence."""

    print "Creating pitch webpage..."

    with codecs.open("docs/pitch.rst", 'w', encoding="utf-8") as out:
        out.write(rst_header(u"Pitch", 1))
        out.write('This page contains basic data of Pitch domain of choros segments such as meter.\n\n')

        AllAndTopComposers = _utils.flatten([['All composers'], topComposers])

        makeAmbitusChart(out, AllSegmentsObj, topComposers, AllAndTopComposers)
        makeConsonanceChart(out, AllSegmentsObj, topComposers, AllAndTopComposers)
        makeIntervalChart(out, AllSegmentsObj, topComposers, AllAndTopComposers)
        makeIntervalSTChart(out, AllSegmentsObj, topComposers, AllAndTopComposers)
        makeLeapsChart(out, AllSegmentsObj, topComposers, AllAndTopComposers)
        makeStepsLeapsChart(out, AllSegmentsObj, topComposers, AllAndTopComposers)
        makeFirstMovementChart(out, AllSegmentsObj, topComposers, AllAndTopComposers)
        makeLastMovementChart(out, AllSegmentsObj, topComposers, AllAndTopComposers)
        makeContourPrimeChart(out, AllSegmentsObj, topComposers, AllAndTopComposers)
        makeDifferentPointsChart(out, AllSegmentsObj, topComposers, AllAndTopComposers)
        makeOscillationChart(out, AllSegmentsObj, topComposers, AllAndTopComposers)
        makeReductionBor355Chart(out, AllSegmentsObj, topComposers, AllAndTopComposers, 8)


def print_lily(out, SegmentObj, subtitle):
    """Write data in a codecs.open object for special_cases page,
    including lilypond file generation."""

    # plotting
    directory = "docs/contour"
    r_composer = SegmentObj.composersStr.replace(" ", "-")
    r_title = SegmentObj.title.replace(" ", "-")
    r_typeof = SegmentObj.typeof
    r_number = str(SegmentObj.number)
    filename = "-".join([r_composer, r_title, r_typeof, r_number])
    dest = _utils.unicode_normalize(os.path.join(directory, filename +  ".png"))
    pngfile = os.path.splitext(os.path.basename(dest))[0]
    SegmentObj.make_score()
    SegmentObj.score.write('png', dest)
    _utils.image_trim(dest)

    midiname = _utils.unicode_normalize(os.path.join(directory, filename +  ".mid"))
    midifile = _utils.unicode_normalize(os.path.join(os.path.basename(directory), filename + ".mid"))
    SegmentObj.midi_save(midiname)

    title = ", ".join([SegmentObj.title, SegmentObj.composersStr, " ".join([SegmentObj.typeof, str(SegmentObj.number)]), subtitle])

    # print in rst
    rst_plot(out, title, pngfile, 4, 90, midifile)


def make_special_cases_webpage(AllSegmentsObj, songsObj):
    """Create and save data of special_cases webpage. The input data
    is an AllSegments object."""

    print "Creating special cases webpage..."

    with codecs.open("docs/special_cases.rst", 'w', encoding="utf-8") as out:
        out.write(rst_header(u"Special cases", 1))
        out.write('This page contains segments with data such as higher and lower ambitus.\n\n')

        # ambitus
        print 'Creating ambitus special cases'
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

        # largest leap
        print 'Creating largest leaps special cases'
        allSemitoneIntervals = AllSegmentsObj.allSemitoneIntervals
        largest_upward_interval = max(allSemitoneIntervals)
        largest_downward_interval = min(allSemitoneIntervals)

        upward_interval_segment = AllSegmentsObj.getBySemitoneInterval(largest_upward_interval).segments[0]
        downward_interval_segment = AllSegmentsObj.getBySemitoneInterval(largest_downward_interval).segments[0]

        out.write(rst_header('Largest leaps', 2))
        out.write(rst_header('Upward', 3))
        print_lily(out, upward_interval_segment, '{0} semitones'.format(largest_upward_interval))
        out.write(rst_header('Downward', 3))
        print_lily(out, downward_interval_segment, '{0} semitones'.format(largest_downward_interval))

        # oscillation contour
        print 'Creating oscillation contour special cases'
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


def loadData(onlyPhrase=True):
    songsObj = retrieval.loadSongs()
    AllSegmentsObj = retrieval.loadSegments()
    if onlyPhrase:
        AllSegmentsObj = AllSegmentsObj.getByTypeOf('Phrase')
    collectionsSeq = json.load(open('songs_map.json'))
    collectionsObj = songcollections.makeAllCollectionSongs(collectionsSeq)
    topComposers = query.composersFilter(AllSegmentsObj, 0.05)

    return songsObj, AllSegmentsObj, collectionsSeq, collectionsObj, topComposers


def singleRun(dataSeq):
    _utils.mkdir('docs/contour')
    songsObj, AllSegmentsObj, collectionsSeq, collectionsObj, topComposers = dataSeq

    make_corpus_webpage(songsObj, collectionsObj)
    make_collections_webpage(collectionsObj)
    make_duration_webpage(AllSegmentsObj, topComposers)
    make_pitch_webpage(AllSegmentsObj, topComposers)
    make_special_cases_webpage(AllSegmentsObj, songsObj)


def run():
    singleRun(loadData())


if __name__ == '__main__':
    run()
