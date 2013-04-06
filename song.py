#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import music21


class Song(object):
    def __init__(self, score, collection, filename):
        self.score = score
        self.piece = score.metadata.title
        self.composer = " ".join(score.metadata.composer.replace('\n', ' ').split())
        self.collection = collection
        self.flatObj = score.flat.notesAndRests
        time_signature_obj = score.flat.getElementsByClass(music21.meter.TimeSignature)[0]
        self.time_signature = time_signature_obj.numerator, time_signature_obj.denominator
        self.filename = filename

    def __repr__(self):
        return "<Song: {0}. {1}>".format(self.piece, self.collection)

    def show(self):
        music21.parse(self.filename).show()


def make_song(xml_name):
    score = music21.parse(xml_name)
    collection = os.path.basename(os.path.dirname(xml_name))
    return Song(score, collection, xml_name)
