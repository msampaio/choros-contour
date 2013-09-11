#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import Counter
from music21.contour import Contour


def counting(seq):
    """Return a collections.Counter object from a sequence of
    values."""

    if type(seq[0]) == Contour:
        seq = [tuple(x) for x in seq]
    return Counter(seq)


# FIXME: Update music21 with contour package to use Sampaio Prime Form
# Algorithm and remove this function
def sampaio(cseg):
    """Return Sampaio contour class prime form."""

    i = cseg.inversion()
    r = cseg.retrogression()
    ri = i.retrogression()
    return Contour(sorted([list(cseg), list(i), list(r), list(ri)])[0])
