#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import music21
import unit
import _utils


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
        self.time_signature = data['time_signature']
        self.meter = data['meter']
        self.pickup = data['pickup']
        self.key = data['key']
        self.mode = data['mode']

        if 'subUnits' in data:
            self.subUnits = data['subUnits']
        else:
            self.subUnits = []

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

    def addMusicUnit(self, subUnit):
        self.subUnits.append(subUnit)
        return self

    def allPhrases(self):
        return [un for un in self.subUnits if un.typeof == 'Phrase']

    def showUnit(self, number, typeof='Phrase'):
        return [un for un in self.subUnits if un.typeof == typeof and un.number == number][0]

    def showBigUnit(self, number, typeof='Period'):
        if typeof == 'Period':
            return [un for un in self.subUnits if un.period_number == number]
        elif typeof == 'Part':
            return [un for un in self.subUnits if un.part_number == number]
        else:
            print 'Wrong typeof {0}'.format(typeof)

    def getAttr(self, attribute):
        return getattr(self, attribute)

    def setAttr(self, attribute, value):
        setattr(self, attribute, value)
        return self

    def getExcerpt(self, initial, final):

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

    def make_score(self, number_show=False):
        if not self.score:
            return makeSong(self.filename, number_show, False)
        else:
            print "There is already a score attribute"
            return self

def makeSong(filename, number_show=False, save=False):

    def get_parameters(measures):
        m1 = measures[0]
        # song data
        params = {}
        params['clef'] = m1.getElementsByClass('Clef')[0]
        params['key_signature'] = m1.getElementsByClass('KeySignature')[0]
        params['time_signature'] = m1.getElementsByClass('TimeSignature')[0]
        return params

    def getSubUnits(filename, songObj, save):
        try:
            data = unit.formParser(filename)
            for el in data:
                el['filename'] = filename
                el['songObj'] = songObj
                el['save'] = save
                subUnit = unit.makeMusicUnit(el)
                songObj.addMusicUnit(subUnit)
            return songObj
        except:
            print "There is no .form file"
            return songObj

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
                    # show enumeration as lyrics
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
    if not save:
        data['score'] = score
        data['measures'] = measures
        data['params'] = params
    else:
        data['score'] = None
        data['params'] = None
        data['measures'] = None
    data['time_signature'] = str(time_signature_obj)
    data['meter'] = time_signature_obj.beatCountName
    data['pickup'] = pickup
    data['key'] = key
    data['mode'] = mode

    return getSubUnits(filename, Song(data), save)


def makeSongCollection(collection, save=False):
    """Returns a list of phrases objects separated by piece.
    """

    files = _utils.filenames_list(collection)
    return [makeSong(f, False, save) for f in files]
