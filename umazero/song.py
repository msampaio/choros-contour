#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import copy
import music21


class Song(object):
    def __init__(self, score, measures, params, pickup, collection, filename):
        self.score = score
        self.title = score.metadata.title
        self.composer = " ".join(score.metadata.composer.replace('\n', ' ').split())
        self.collection = collection
        self.measures = measures
        self.params = params
        self.pickup = pickup
        time_signature_obj = self.params['time_signature']
        self.time_signature = time_signature_obj.numerator, time_signature_obj.denominator
        self.key_signature = self.params['key_signature'].sharps
        self.filename = filename

    def __repr__(self):
        return "<Song: {0}. {1}>".format(self.title, self.collection)

    def show(self, arg=None):
        self.score.show(arg)

    def xml_write(self, suffix='numbered', path=None):
        dirname = os.path.dirname(self.filename)
        basename = os.path.basename(self.filename).split('.')[0] + ' - {0}.xml'.format(suffix)
        if path:
            dirname = path
        dest = os.path.join(dirname, basename)
        print "Writing xml file in {0}".format(dest)
        self.score.write('musicxml', dest)

    def get_phrase(self, initial, final):

        def make_measure(measure, params, keep_list, n):
            new_measure = music21.stream.Measure()
            if measure.number == 0:
                new_measure.pickup = True
            else:
                new_measure.pickup = None
            # insert params only in phrase first measure
            if n == 0:
                for values in params.values():
                    new_measure.append(values)
            for event in measure.notesAndRests:
                if event.event_number in keep_list:
                    new_measure.append(event)
            if measure.notesAndRests[0] != new_measure.notesAndRests[0]:
                new_measure.pickup = True

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
        new_score.pickup = False

        measure_number = 1
        first_measure = 0

        for n, measure in enumerate(measures):
            if any([(ev in keep_list) for ev in measure.events]):
                first_measure += 1
                if first_measure == 1:
                    n = 0
                new_measure = make_measure(measure, params, keep_list, n)
                if new_measure.pickup:
                    new_score.pickup = True
                    new_measure.pickup = None
                    new_measure.number = 0
                    measure_number = 0
                else:
                    new_measure.number = measure_number
                measure_number += 1
                new_score.append(new_measure)

        return new_score


def make_song(xml_name, number_show=False):

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

    if measures[0].number == 0:
        pickup = True
    else:
        pickup = False

    event_n = 0
    for measure in part:
        if type(measure) == music21.stream.Measure:
            measure_events = []
            for el in measure:
                if type(el) in (music21.note.Note, music21.note.Rest):
                    event_n += 1
                    el.event_number = event_n
                    if number_show:
                        el.lyric = event_n
                    measure_events.append(event_n)
            measure.events = measure_events
    collection = os.path.basename(os.path.dirname(xml_name))
    return Song(score, measures, params, pickup, collection, xml_name)
