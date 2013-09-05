#!/usr/bin/env python
# -*- coding: utf-8 -*-

import music21


def sourceParse(filename):
    return music21.converter.parse(filename)
