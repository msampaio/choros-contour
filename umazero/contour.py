#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import Counter
from music21.contour import Contour
import _utils


def counting(seq):
    if type(seq[0]) == Contour:
        seq = [tuple(x) for x in seq]
    return Counter(seq)


def contour_prime_count(units):
    return counting([un.contour.reduction_morris()[0] for un in units])


def contour_highest_cp_count(units):
    return counting([max(un.contour.translation()) for un in units])


def passing_contour(units):
    result = []
    for unit in units:
        reduced = unit.contour.reduction_bor(3)
        size = unit.contour_size
        reduced_size = len(reduced)
        result.append(1 - (reduced_size / float(size)))
    return counting(result)
