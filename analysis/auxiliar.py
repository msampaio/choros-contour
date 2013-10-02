#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
from collections import Counter
import music


class ExtCounter(object):
    """Extended Counter class."""

    def __init__(self):
        self.counter = None
        self.musicalParameter = None
        self.originalClass = None

    def __repr__(self):
        return "<Counter {0} {1}>".format(self.musicalParameter, self.originalClass)

    def percentual(self):
        """Return a Counter object with percent values"""

        def perc(val, total):
            return val * 100.0 / total

        newExtCounter = copy.deepcopy(self)
        total = sum(newExtCounter.counter.values())

        for k, v in newExtCounter.counter.items():
            newExtCounter.counter[k] = perc(v, total)

        return newExtCounter

    def groupOthers(self, minimum=0.1):
        m = minimum * 100
        percentualCounter = self.percentual()
        newCounter = copy.copy(self.counter)
        othersValues = 0
        loopCounter = 0

        for k, v in percentualCounter.counter.items():
            if v <= m:
                loopCounter += 1
                othersValues += self.counter[k]
                del newCounter[k]

        if loopCounter > 1:
            newCounter['Others'] = othersValues
            r = makeExtCounter(newCounter, self.musicalParameter, self.originalClass)
        else:
            r = self

        return r

    def show(self):
        for k, v in self.counter.items():
            print '{0}: {1}'.format(k, v)


def makeExtCounter(data, musicalParameter=None, originalClass=None):
    """Return an ExtCounter object from a given data and optionals
    arguments."""

    data = music.contourSequenceToTuple(data)

    extCounter = ExtCounter()
    extCounter.counter = Counter(data)
    extCounter.musicalParameter = musicalParameter
    extCounter.originalClass = originalClass

    return extCounter
