#!/usr/bin/env python

import matplotlib
import matplotlib.pyplot as plt
import pylab
from music21.contour import Contour
import _utils
from collections import Counter


def __explode_max(data):
    maximum = max(data)
    return [0.05 if el == maximum else 0 for el in data]


def clear():
    """Clear plot image."""

    pylab.clf()


def simple_pie(values, labels=None, title=None, filename=None):
    """Accepts a sequence of values."""
    
    range_numbers = range(len(values))
    # make a square figure and axes
    plt.figure(1, figsize=(6,6))

    if not labels:
        labels = [j + 1 for j in range_numbers]

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


def simple_scatter(y, x, title=None, filename=None):
    """Accepts a sequence of two sequences of values."""

    range_numbers = range(len(x))
    # make a square figure and axes
    plt.figure(1, figsize=(4,4))

    # if not labels:
    #     labels = [j + 1 for j in range_numbers]

    # x, y = values
    plt.scatter(x, y, c='k')

    if title:
        plt.title(title, bbox={'facecolor':'0.8', 'pad':5})

    if not filename:
        filename = '/tmp/foo.png'
    plt.savefig(filename, dpi=72)
