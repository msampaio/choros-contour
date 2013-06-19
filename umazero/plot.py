#!/usr/bin/env python

import numpy
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import pylab
from music21.contour import Contour
from collections import Counter
import copy
import _utils


def __explode_max(seq):
    """Return a sequence of values for pie chart explode from a given
    sequence."""

    maximum = max(seq)
    return [0.05 if el == maximum else 0 for el in seq]


def clear():
    """Clear plot image."""

    pylab.clf()


def simple_pie(values, labels=None, title=None, filename=None):
    """Plot a pie chart. The input data is a sequence of values."""
    
    range_numbers = range(len(values))
    # make a square figure and axes
    plt.figure(1, figsize=(6,6))

    if not labels:
        labels = [j + 1 for j in range_numbers]
    else:
        if type(labels[0]) == tuple:
            new = []
            for el in labels:
                if el != 'Others':
                    el = Contour(el)
                new.append(el)
            labels = new

    explode_seq = [0 for k in range_numbers]
    explode_seq[values.index(max(values))] = 0.05
    explode=tuple(explode_seq)

    colors = ("#D7EEA4", "#00BF40", "#FFAC00", "#FF4100", "#009AB7", "#AE005C")

    plt.pie(values, explode=explode, labels=labels,
                    autopct='%1.1f%%', shadow=True, startangle=90, colors=colors)
                    # The default startangle is 0, which would start
                    # the Frogs slice on the x-axis.  With startangle=90,
                    # everything is rotated counter-clockwise by 90 degrees,
                    # so the plotting starts on the positive y-axis.

    if title:
        plt.title(title, bbox={'facecolor':'0.8', 'pad':5})

    if not filename:
        filename = '/tmp/foo.png'
    plt.savefig(filename, dpi=72)


def simple_scatter(y, x, labels, title=None, filename=None):
    """Plot a scatter chart. The input data is two sequences of
    values, and a sequence of labels for y and x axis."""

    range_numbers = range(len(x))
    # make a square figure and axes
    plt.figure(1, figsize=(4,4))

    # FIXME: use values between 10 and 500
    area = [i * 5 for i in y]
    plt.scatter(x, _utils.percentual(y), s=area, c='k')

    if title:
        plt.title(title, bbox={'facecolor':'0.8', 'pad':5})

    if labels:
        plt.xlabel(labels[1])
        plt.ylabel(labels[0])

    if not filename:
        filename = '/tmp/foo.png'
    plt.savefig(filename, dpi=72)


def stacked_bars(stackedDic=stackedDic):

    values = stackedDic['values']
    labels = stackedDic['labels']
    title = stackedDic['title']
    ylabel = stackedDic['ylabel']
    xticks = stackedDic['xticks']

    def multiple_bottom(values):
        """Return a sequence with bottoms to stacked bars."""

        bottomSeq = []
        for n in range(len(values)):
            if n == 0:
                bottomSeq.append(0)
            else:
                seq = values[:n]
                if len(seq) == 1:
                    val = seq[0]
                else:
                    val = tuple([sum(zipped) for zipped in zip(*seq)])
                bottomSeq.append(val)

        return bottomSeq

    ind = numpy.arange(len(values[0]))
    width = 0.35       # the width of the bars: can also be len(x) sequence

    # bottom values
    bottomSeq = multiple_bottom(values)

    maxValue = max([sum(vals) for vals in zip(bottomSeq[-1], values[-1])])

    # plot
    plots = []
    c = 0 # color
    for n, seq in enumerate(values):
        plots.append(plt.bar(ind, seq, width, color=cm.jet(c), bottom=bottomSeq[n]))
        c += 20

    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(ind+width/2., xticks, rotation=90)
    plt.yticks(numpy.arange(0, maxValue, maxValue / 10))
    plt.legend([x[0] for x in plots], labels)

    plt.show()

def generateStackedDic(allSegmentObj, attrib='pickup', topComposers=['Pixinguinha', 'Waldyr Azevedo'], commonNumber=4):
    """Return a dictionary with data for stacked_bars function."""

    def generateCounted(allSegmentObj, composer):
        if composer == 'All Composers':
            return allSegmentObj
        else:
            return allSegmentObj.getByComposer(composer)

    # FIXME: create 'other' for less present values

    composers = copy.deepcopy(topComposers)
    # composers.insert(0, 'All Composers')

    valuesData = {}
    commonElements = set()

    for composer in composers:
        composerSegmentsSeq = generateCounted(allSegmentObj, composer).segments
        if attrib in ('contour', 'contour_prime'):
            val = [tuple(getattr(seg, attrib)) for seg in composerSegmentsSeq]
        else:
            val = [getattr(seg, attrib) for seg in composerSegmentsSeq]

        counted = Counter(val)
        most_common = counted.most_common()[:commonNumber]
        newCounted = _utils.group_minorities(counted, 0.05)
        valuesData[composer] = newCounted
        for k, v in most_common:
            commonElements.add(k)

    commonElements = sorted(commonElements)
    valuesSeq = []

    for commonEl in commonElements:
        commonElSeq = []
        for vComposer, vCounter in sorted(valuesData.items()):
            commonElSeq.append(vCounter[commonEl])
        valuesSeq.append(commonElSeq)

    if attrib in ('contour', 'contour_prime'):
        commonElements = [Contour(cseg) for cseg in commonElements]
    else:
        commonElements = list(commonElements)

    stackedDic = {}
    stackedDic['xticks'] = composers
    stackedDic['labels'] = commonElements
    stackedDic['ylabel'] = 'Segments number'
    stackedDic['title'] = 'Segments by {0}'.format(attrib)
    stackedDic['values'] = valuesSeq

    return stackedDic

def simple_stacked_bar(allSegmentObj, attrib, topComposers, commonNumber=4):
    """Return a stacked bar chard from given data."""

    stackedDic = generateStackedDic(allSegmentObj, attrib, topComposers, commonNumber)
    stacked_bars(stackedDic)
