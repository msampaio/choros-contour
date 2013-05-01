#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import Counter


def is_consonant(interval):
    consonants = "2 3 6".split()

    quality = interval[0]
    quantity = interval[1:]

    if quality == "P":
        return True
    elif quality == "M" or quality == "m" and quantity in consonants:
        return True
    else:
        return False


def is_leap(interval):
    """Return True if a given interval is a leap."""

    non_leap = "1 2 3".split()

    if interval[1:] in non_leap:
        return False
    else:
        return True


def single_step_leap_arpeggio(interval):
    """Return the classification of a given interval as step, leap or
    arpeggio (3rds)."""

    value = interval[1:]
    if is_leap(interval):
        return 'Leap'
    elif value == '1':
        return 'Repetition'
    elif value == '3':
        return '3rd'
    else:
        return 'Step'


def leaps(intervals_seq):
    """Return a collections.Counter object with leaps from a given
    sequence of intervals."""

    return Counter((i for i in intervals_seq if is_leap(i)))


def step_leap_arpeggio(intervals_seq):
    """Return a collections.Counter object with steps, thirds and
    leaps from a given sequence of intervals."""

    return Counter((single_step_leap_arpeggio(i) for i in intervals_seq))
