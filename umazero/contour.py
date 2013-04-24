#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import Counter
from music21.contour import Contour
import _utils


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


def contour_prime_count(MusicUnitsList):
    """Return a collections.Counter object with prime contours from a
    list of MusicUnit objects."""

    return counting([sampaio(un.contour.reduction_morris()[0]) for un in MusicUnitsList])


def contour_highest_cp_count(MusicUnitsList):
    """Return a collections.Counter object with the values of highest
    contour point of each contour segment from a list of MusicUnit
    objects."""

    return counting([max(un.contour.translation()) for un in MusicUnitsList])


def contour_oscillation_count(MusicUnitsList):
    """Return a collections.Counter object with the values of
    oscilattion index of each contour segment from a list of MusicUnit
    objects."""

    return counting([MusicUnitObj.contour.oscillation_index() for MusicUnitObj in MusicUnitsList])


def first_movement(MusicUnitsList):
    """Return a collections.Counter object with the values of first
    two contour points ascent/descent movement of each contour segment
    from a list of MusicUnit objects."""

    return counting([MusicUnitObj.contour.internal_diagonals()[0] for MusicUnitObj in MusicUnitsList])


def last_movement(MusicUnitsList):
    """Return a collections.Counter object with the values of last two
    contour points ascent/descent movement of each contour segment
    from a list of MusicUnit objects."""

    return counting([MusicUnitObj.contour.internal_diagonals()[-1] for MusicUnitObj in MusicUnitsList])


def passing_contour(MusicUnitObj):
    """Return an index of a proportion of 'passing contour point' in a
    contour segment based on Window-3 reduction algorithm.. The input
    argument is a MusicUnit object."""

    reduced = MusicUnitObj.contour.reduction_bor(3)
    size = MusicUnitObj.contour_size
    reduced_size = len(reduced)
    return 1 - (reduced_size / float(size))


def multicount(MusicUnitsList, fn):
    """Return a collections.Counter object with the values calculated
    with the 'fn' function in a list of MusicUnit objects."""

    return counting([fn(MusicUnitObj) for MusicUnitObj in MusicUnitsList])
