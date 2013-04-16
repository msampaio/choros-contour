#!/usr/bin/env python
# -*- coding: utf-8 -*-

import song


class MusicUnit(song.Song):
    def __init__(self, data):

        self.filename = data['filename']

        # metadata
        self.collection = data['collection']
        self.title = data['title']
        self.composer = data['composer']

        # music
        self.score = data['score']
        self.time_signature = data['time_signature']
        self.meter = data['meter']
        self.pickup = data['pickup']

        self.typeof = data['typeof']
        self.number = data['number']

        self.initial_event = data['initial_event']
        self.final_event = data['final_event']

        self.part_number = data['part_number']
        self.period_number = data['period_number']

    def __repr__(self):
        return "<Unit {0}: {1} - {2} ({3})>".format(self.typeof, self.title, self.composer, self.number)

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


def makeMusicUnit(data_input):
    initial = data_input['initial']
    final = data_input['final']

    songObj = data_input['songObj']
    score = songObj.getExcerpt(initial, final)
    
    data = {}

    data['filename'] = songObj.filename

    # metadata
    data['collection'] = songObj.collection
    data['title'] = songObj.title
    data['composer'] = songObj.composer

    # music
    if not data_input['save']:
        data['score'] = score
    else:
        data['score'] = None

    data['time_signature'] = songObj.time_signature
    data['meter'] = songObj.meter
    data['pickup'] = score.pickup

    # analysis
    data['typeof'] = data_input['typeof']
    data['number'] = data_input['number']
    data['initial_event'] = initial
    data['final_event'] = final
    data['part_number'] = data_input['part_number']
    data['period_number'] = data_input['period_number']

    return MusicUnit(data)


def formParser(filename):
    form_name = filename.strip('.xml') + '.form'
    with open(form_name, 'r') as f:
        seq = [el.strip('\n') for el in f.readlines() if el.strip('\n')]
    form = []
    part_number = 0
    period_number = 0
    phrase_number = 0
    link_number = 0

    for el in seq:
        if el == '# part':
            part_number += 1
        elif el == '# period':
            period_number += 1
        else:
            typeof, i, f = el.split()
            initial = int(i)
            final = int(f)
            dic = {}
            dic['initial'] = initial
            dic['final'] = final
            dic['period_number'] = period_number
            dic['part_number'] = part_number
            if typeof == 'p':
                phrase_number += 1
                dic['typeof'] = 'Phrase'
                dic['number'] = phrase_number
            else:
                link_number += 1
                dic['typeof'] = 'Link'
                dic['number'] = link_number
            form.append(dic)

    return form
