#!/usr/bin/env python
# -*- coding: utf-8 -*-

import core
import _utils
from collections import defaultdict


def phrase_contour_reduction(pickle_file):
    phrases = core.load_pickle(pickle_file)
    all_phrases = _utils.flatten(phrases)
    return [phr.contour.reduction_morris()[0] for phr in all_phrases]

def sort_phrases(contour_list):
    # loop duplication

    size = len(contour_list)

    d = defaultdict(int)
    for cseg in contour_list:
        el = tuple(cseg)
        d[el] += 1

    sorted_data = sorted(d.items(), key=lambda x: x[1], reverse=True)
    print "Cseg --- percentage --- ocurrences"
    for t_cseg, n in sorted_data:
        cseg = core.Contour(t_cseg)
        percentage = n / float(size) * 100
        print "{0} {1:.2f}% ({2})".format(cseg, percentage, n)


if __name__ == '__main__':
    pickle_file = 'pixinguinha'
    data = phrase_contour_reduction(pickle_file)
    sort_phrases(data)
