#!/usr/bin/env python
# -*- coding: utf-8 -*-

import music21
import _utils


def sourceParse(filename):
    return music21.converter.parse(filename)


def formParse(filename):
    """Returns a dictionary with the formal structure of a song
    parsed. The argument is the name of xml file, but the function
    parses the .form file in the same directory of the xml one."""

    formName = _utils.changeSuffix(filename, 'form')

    with open(formName, 'r') as f:
        lines = f.readlines()
        seq = []
        for el in lines:
            seq_el = _utils.remove_endline(el).strip(' ')
            if seq_el not in [' ', '']:
                seq.append(seq_el)
    form = []
    segment_number = 0

    for el in seq:
        if list(el)[0] != '#':
            typeof, i, f = el.split()
            initial = int(i)
            final = int(f)
            segment_number += 1

            segment_form = {}
            segment_form['initial'] = initial
            segment_form['final'] = final
            segment_form['number'] = segment_number

            if typeof == 'p':
                segment_form['typeof'] = 'Phrase'
            else:
                segment_form['typeof'] = 'NonPhrase'
            form.append(segment_form)

    return form
