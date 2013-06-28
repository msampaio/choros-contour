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


def pie(values, labels=None, title=None):
    """Return plt object with a pie chart. The input data is a
    sequence of values."""

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

    return plt


def pieSave(values, labels=None, title=None, filename=None):
    """Plot a pie chart. The input data is a sequence of values."""

    plt = pie(values, labels=None, title=None)

    if not filename:
        filename = '/tmp/foo.png'
    plt.savefig(filename, dpi=72)


def scatter(y, x, labels=None, title=None):
    """Return a plt object with a scatter chart. The input data is two
    sequences of values, and a sequence of labels for y and x axis.

    >>> scatter([1, 2, 3], [4, 5, 6], ['Y axis', 'X axis'])
    """

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

    return plt


def scatterSave(y, x, labels, title=None, filename=None):
    """Plot a scatter chart. The input data is two sequences of
    values, and a sequence of labels for y and x axis."""

    plt = scatter(y, x, labels, title=None)

    if not filename:
        filename = '/tmp/foo.png'
    plt.savefig(filename, dpi=72)


def multipleScatter(coordSequence, labels, legend, title=None):
    """Return a plt object with multiple superposed scatter charts.
    The input data is a sequence of (y, x) coordinates, labels for y
    and x axis, and a legend with plotted data.

    multipleScatter([[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]]],
       ['Y axis', 'X axis'], ['Group A', 'Group B'], 'Title')
    """

    fig = plt.figure(figsize=(10,5))
    ax = plt.subplot(111)

    plots = []
    color_increment = int(250 / float(len(legend)))
    c = 0 # color

    for y, x in coordSequence:
        area = [i * 5 for i in y]
        plots.append(plt.scatter(x, _utils.percentual(y), s=area, color=cm.jet(c)))
        c += color_increment

    plt.title(title)
    plt.xlabel(labels[1])
    plt.ylabel(labels[0])

    # Shink current axis by 25%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.75, box.height])

    # Put a legend to the right of the current axis
    ax.legend(legend, loc='center left', bbox_to_anchor=(1, 0.5))

    return plt


def multipleScatterSave(coordSequence, labels, legend, title=None, filename=None):
    """Plot a scatter chart. The input data is two sequences of
    values, and a sequence of labels for y and x axis."""

    plt = multipleScatter(coordSequence, labels, legend, title)

    if not filename:
        filename = '/tmp/foo.png'
    plt.savefig(filename, dpi=72)


def stacked_bars(stackedDic):

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
    width = 0.45       # the width of the bars: can also be len(x) sequence

    # bottom values
    bottomSeq = multiple_bottom(values)

    cleaned_values = [val for val in values if val]
    maxValue = max([sum(vals) for vals in zip(*cleaned_values) if vals])

    # plot
    plots = []

    color_increment = int(250 / float(len(labels)))
    c = 0 # color

    fig = plt.figure()
    ax = plt.subplot(111)

    for n, seq in enumerate(values):
        plots.append(ax.bar(ind, seq, width, color=cm.jet(c), bottom=bottomSeq[n]))
        c += color_increment

    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(ind+width/2., xticks, rotation=90)
    plt.yticks(numpy.arange(0, maxValue * 1.1, maxValue / 10))

    # Shink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 * 3, box.width * 0.8, box.height * 0.75])

    # Put a legend to the right of the current axis
    ax.legend([x[0] for x in plots], labels, loc='center left', bbox_to_anchor=(1, 0.5))

    return plt


def stackedBarSave(stackedDic):

    plt = stacked_bars(stackedDic)

    if 'filename' in stackedDic:
        filename = stackedDic['filename']
    else:
        filename = '/tmp/foo.png'

    plt.savefig(filename, dpi=72)


def generateAttribStackedDic(allSegmentObj, topComposers, attrib, valuesNumber=5, title='', ylabel='Segments', filename=None):

    values, labels, xticks = _utils.attribValuesMatrix(allSegmentObj, topComposers, attrib, valuesNumber)
    stackedDic = {}
    stackedDic['values'] = values
    stackedDic['labels'] = labels
    stackedDic['title'] = title
    stackedDic['ylabel'] = ylabel
    stackedDic['xticks'] = xticks
    stackedDic['filename'] = filename

    return stackedDic


def attribStackedBarSave(allSegmentObj, attrib, topComposers, valuesNumber=4, title='', ylabel='Segments', filename=None):
    """Return a stacked bar chard from given data."""

    stackedDic = generateAttribStackedDic(allSegmentObj, topComposers, attrib, valuesNumber, title, ylabel, filename)
    stackedBarSave(stackedDic)
