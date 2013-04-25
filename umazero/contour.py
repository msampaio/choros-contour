#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import Counter
from music21.contour import Contour
from music21.contour import comparison
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


def contour_prime_count(SegmentsList):
    """Return a collections.Counter object with prime contours from a
    list of Segment objects."""

    return counting([sampaio(seg.contour.reduction_morris()[0]) for seg in SegmentsList])


def contour_highest_cp_count(SegmentsList):
    """Return a collections.Counter object with the values of highest
    contour point of each contour segment from a list of Segment
    objects."""

    return counting([max(seg.contour.translation()) for seg in SegmentsList])


def contour_oscillation_count(SegmentsList):
    """Return a collections.Counter object with the values of
    oscilattion index of each contour segment from a list of Segment
    objects."""

    return counting([SegmentObj.contour.oscillation_index() for SegmentObj in SegmentsList])


def first_movement(SegmentsList):
    """Return a collections.Counter object with the values of first
    two contour points ascent/descent movement of each contour segment
    from a list of Segment objects."""

    return counting([SegmentObj.contour.internal_diagonals()[0] for SegmentObj in SegmentsList])


def last_movement(SegmentsList):
    """Return a collections.Counter object with the values of last two
    contour points ascent/descent movement of each contour segment
    from a list of Segment objects."""

    return counting([SegmentObj.contour.internal_diagonals()[-1] for SegmentObj in SegmentsList])


def passing_contour(SegmentObj):
    """Return an index of a proportion of 'passing contour point' in a
    contour segment based on Window-3 reduction algorithm.. The input
    argument is a Segment object."""

    reduced = SegmentObj.contour.reduction_bor(3)
    size = SegmentObj.contour_size
    reduced_size = len(reduced)
    return 1 - (reduced_size / float(size))


def multicount(SegmentsList, fn):
    """Return a collections.Counter object with the values calculated
    with the 'fn' function in a list of Segment objects."""

    return counting([fn(SegmentObj) for SegmentObj in SegmentsList])


def period_comparison(periodsList):
    """Return a list of tuples with phrases period and acmemb value
    between them. The input data is a list of periods."""

    result = []
    for period in periodsList:
        phrases = [segment for segment in period if segment.typeof == 'Phrase']
        # FIXME: improve acmemb algorithm to compare contours instead of primes
        primes = [phrase.contour.reduction_morris()[0] for phrase in phrases]
        # FIXME: use Schultz instead of reduction_morris to remove this condition
        if len(primes[0]) < 10 and len(primes[1]) < 10:
            acmemb = comparison.all_contour_mutually_embedded(*primes)
            if acmemb != 1:
                result.append((phrases, acmemb))
    return sorted(result, key=lambda x: x[1])
