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

    def get_phrase(self, initial, final):

        def remove_events(measure, keep_list):
            for event in measure:
                if type(event) is music21.note.Note:
                # if type(event) in (music21.note.Note, music21.note.Rest):
                    if event.event_number not in keep_list:
                        # why can't I remove note from measure?
                        measure.remove(event)

        part = self.score.parts[0]
        keep_list = range(initial, final + 1)

        phrase_measures = []
        for measure in part:
            if type(measure) == music21.stream.Measure:
                if initial in measure.events or final in measure.events:
                    remove_events(measure, keep_list)
                    phrase_measures.append(measure.number)
        measures = range(phrase_measures[0], phrase_measures[1] + 1)

        sNew = music21.stream.Stream()
        for m in part:
            if type(m) == music21.stream.Measure and m.number in measures:
                sNew.append(m)
        return sNew


def make_song(xml_name):
    score = music21.parse(xml_name)
    part = score.getElementsByClass('Part')[0]
    event = 0
    for measure in part:
        if type(measure) == music21.stream.Measure:
            measure_events = []
            for el in measure:
                if type(el) in (music21.note.Note, music21.note.Rest):
                    event += 1
                    el.event_number = event
                    measure_events.append(event)
            measure.events = measure_events
    collection = os.path.basename(os.path.dirname(xml_name))
    return Song(score, collection, xml_name)
