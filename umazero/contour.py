#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import Counter
from music21.contour import Contour
import _utils


def counting(seq):
    if type(seq[0]) == Contour:
        seq = [tuple(x) for x in seq]
    return Counter(seq)


def contour_prime_count(phrases):
    return counting([phr.contour.reduction_morris()[0] for phr in phrases])


def contour_highest_cp_count(phrases):
    return counting([max(phr.contour.translation()) for phr in phrases])


def passing_contour(phrases):
    result = []
    for phrase in phrases:
        reduced = phrase.contour.reduction_bor(3)
        size = phrase.contour_size
        reduced_size = len(reduced)
        result.append(1 - (reduced_size / float(size)))
    return counting(result)
