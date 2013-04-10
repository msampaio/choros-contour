#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import copy
import music21


class Song(object):
    def __init__(self, score, measures, params, collection, filename):
        self.score = score
        self.title = score.metadata.title
        self.composer = " ".join(score.metadata.composer.replace('\n', ' ').split())
        self.collection = collection
        self.measures = measures
        self.params = params
        time_signature_obj = self.params['time_signature']
        self.time_signature = time_signature_obj.numerator, time_signature_obj.denominator
        self.key_signature = self.params['key_signature'].sharps
        self.filename = filename

    def __repr__(self):
        return "<Song: {0}. {1}>".format(self.title, self.collection)

    def show(self, arg=None):
        music21.parse(self.filename).show(arg)

    def get_phrase(self, initial, final):

        def make_measure(measure, params, keep_list, n):
            new_measure = music21.stream.Measure()
            # insert params only in phrase first measure
            if n == 1:
                for values in params.values():
                    new_measure.append(values)
            for el in measure.notesAndRests:
                if el.event_number in keep_list:
                    new_measure.append(el)
            return new_measure

        def make_stream(measures):
            new_score = music21.stream.Stream()
            for measure in measures:
                new_score.append(measure)
            return new_score

        keep_list = range(initial, final + 1)
        measures = self.measures
        params = self.params

        new_score = music21.stream.Stream()
        new_score.initial = initial
        new_score.final = final

        for n, measure in enumerate(measures):
            if any([(ev in keep_list) for ev in measure.events]):
                new_score.append(make_measure(measure, params, keep_list, n))

        return new_score


def make_song(xml_name):

    def get_parameters(measures):
        m1 = measures[0]
        # song data
        params = {}
        params['clef'] = m1.getElementsByClass('Clef')[0]
        params['key_signature'] = m1.getElementsByClass('KeySignature')[0]
        params['time_signature'] = m1.getElementsByClass('TimeSignature')[0]
        return params

    score = music21.parse(xml_name)
    part = score.getElementsByClass('Part')[0]
    measures = part.getElementsByClass('Measure')
    params = get_parameters(measures)
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
    return Song(score, measures, params, collection, xml_name)
