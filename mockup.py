#!/usr/bin/env python
# -*- coding: utf-8 -*-

import core


def make_all_phrases():
    files_list = core.files_list()
    return [core.make_phrases(f) for f in files_list]


def phrase_contour_reduction(phrases):
    return [phr.contour.reduction_morris() for phr in phrases]
