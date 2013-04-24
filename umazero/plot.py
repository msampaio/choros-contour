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


def stacked_bars(stacked_bar_data):
    """Plot a chart with stacked bars. The input data is a dictionary
    with values, legend_labels, bas_legend, title and ylabel data."""

    values = stacked_bar_data['values']
    legend_labels = stacked_bar_data['legend_labels']
    bars_legend = stacked_bar_data['bars_legend']
    size = len(values[0])

    higher_bar = max([sum([line[i] for line in values]) for i in range(size)])

    for bl in bars_legend:
        if len(bl) > 40:
            splitted = bl.split()
            words = len(splitted)
            half = words / 2
            word_ind = bars_legend.index(bl)
            bars_legend[word_ind] = "\n".join([" ".join(splitted[:half]), " ".join(splitted[half:])])

    title = stacked_bar_data['title']
    ylabel = stacked_bar_data['ylabel']

    ind = numpy.arange(size)    # the x locations for the groups
    width = 0.35       # the width of the bars: can also be len(x) sequence

    c = 0
    legend = []
    plt.figure(1, figsize=(10,8))
    for val in values:
        p = plt.bar(ind, val, width, color=cm.jet(c))
        # FIXME: improve increment
        c += 20
        legend.append(p[0])

    plt.ylabel(ylabel)
    plt.title(title)

    plt.xticks(ind+width/2., bars_legend, rotation=90, fontsize=10)
    plt.yticks(numpy.arange(0,81,10))
    plt.legend(legend, legend_labels)
    plt.subplots_adjust(left=None, right=None, bottom=0.4, top=0.9, wspace=None, hspace=None)
    plt.ylim(0, higher_bar * 1.2)
    plt.show()


def generate_stacked_bar_data(AllMusicUnitsObj, attrib):
    """Return a dictionary with data for stacked_bars function. The
    input data is an AllMusicUnits object and the attribute from this
    object to be plotted in stacked bars."""

    AllMusicUnitsObj = copy.deepcopy(AllMusicUnitsObj)
    attrib_values = []
    composers = AllMusicUnitsObj.allComposers
    composers_values = {}
    for MusicUnitObj in AllMusicUnitsObj.units:
        value = getattr(MusicUnitObj, attrib)
        composer = MusicUnitObj.composer
        if not value in composers_values:
            composers_values[value] = [0 for c in composers]
        ind = composers.index(composer)
        composers_values[value][ind] += 1
        attrib_values.append(value)
    ordered_attrib_values = [val[0] for val in Counter(attrib_values).most_common()]
    stacked_bar_data = {}
    stacked_bar_data['title'] = attrib[0].upper() + attrib[1:]
    stacked_bar_data['ylabel'] = 'MusicUnits'
    stacked_bar_data['bars_legend'] = composers
    stacked_bar_data['legend_labels'] = ordered_attrib_values
    stacked_bar_data['values'] = []
    for val in ordered_attrib_values:
        stacked_bar_data['values'].append(composers_values[val])
    # FIXME: create all and other categories

    return stacked_bar_data

def stacked_bar_chart(AllMusicUnitsObj, attrib):
    """Return a stacked bar chart from a given AllMusicUnits object
    and a given attribute name from this object to be plotted in
    stacked bars."""

    stacked_bars(generate_stacked_bar_data(AllMusicUnitsObj, attrib))
