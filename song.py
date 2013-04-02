#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import music21


def m21_data(xml_name):
    """Returns Music21 data (flatten stream object, piece name,
    composer) and collection from a given xml file path.
    """

    song = music21.parse(xml_name)
    piece = song.metadata.title
    composer = song.metadata.composer
    collection = os.path.basename(os.path.dirname(xml_name))
    flatten_obj = song.flat.notesAndRests
    time_signature_obj = song.flat.getElementsByClass(music21.meter.TimeSignature)[0]
    time_signature = time_signature_obj.numerator, time_signature_obj.denominator

    return flatten_obj, piece, composer, collection, time_signature
