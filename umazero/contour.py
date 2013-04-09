#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import Counter
from music21.contour import Contour
import _utils
import phrase
import data


def counting(seq):
    if type(seq[0]) == Contour:
        seq = [tuple(x) for x in seq]
    return Counter(seq)


def contour_prime_count(phrases):
    return counting([phr.contour.reduction_morris()[0] for phr in phrases])


def contour_highest_cp_count(phrases):
    return counting([max(phr.contour.translation()) for phr in phrases])
