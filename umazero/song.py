#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import music21


class Song(object):
    def __init__(self, data):

        self.filename = data['filename']

        # metadata
        self.collection = data['collection']
        self.title = data['title']
        self.composer = data['composer']

        # music
        self.score = data['score']
        self.measures = data['measures']
        self.params = data['params']
        self.time = data['time_signature']
        self.meter = data['meter']
        self.pickup = data['pickup']
        self.key = data['key']
        self.mode = data['mode']

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


def make_song(filename, number_show=False):

    def get_parameters(measures):
        m1 = measures[0]
        # song data
        params = {}
        params['clef'] = m1.getElementsByClass('Clef')[0]
        params['key_signature'] = m1.getElementsByClass('KeySignature')[0]
        params['time_signature'] = m1.getElementsByClass('TimeSignature')[0]
        return params

    score = music21.parse(filename)
    part = score.getElementsByClass('Part')[0]
    measures = part.getElementsByClass('Measure')
    params = get_parameters(measures)
    time_signature_obj = params['time_signature']
    key, mode = params['key_signature'].pitchAndMode

    if measures[0].number == 0:
        pickup = True
    else:
        pickup = False

    # enumerate events
    event_n = 0
    for measure in part:
        if type(measure) == music21.stream.Measure:
            measure_events = []
            for el in measure:
                if type(el) in (music21.note.Note, music21.note.Rest):
                    event_n += 1
                    el.event_number = event_n
                    # show enumeation as lyrics
                    if number_show:
                        el.lyric = event_n
                    measure_events.append(event_n)
            measure.events = measure_events

    data = {}
    data['filename'] = filename

    # metadata
    data['collection'] = os.path.basename(os.path.dirname(filename))
    data['title'] = score.metadata.title
    data['composer'] = " ".join(score.metadata.composer.replace('\n', ' ').split())

    # music
    data['score'] = score
    data['measures'] = measures
    data['params'] = params
    data['time_signature'] = str(time_signature_obj)
    data['meter'] = time_signature_obj.beatCountName
    data['pickup'] = pickup
    data['key'] = key
    data['mode'] = mode

    return Song(data)
