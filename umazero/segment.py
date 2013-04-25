#!/usr/bin/env python
# -*- coding: utf-8 -*-

from music21.contour import Contour
import song
import _utils


class Segment(song.Song):
    """Class for Segment classes. A segment is a phrase or link of a
    song."""

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
        self.ambitus = data['ambitus']
        self.pickup = data['pickup']

        self.contour = data['contour']
        self.contour_prime = data['contour_prime']
        self.contour_size = data['contour_size']

        self.typeof = data['typeof']
        self.number = data['number']

        self.initial_event = data['initial_event']
        self.final_event = data['final_event']

        self.part_number = data['part_number']
        self.period_number = data['period_number']

    def __repr__(self):
        return "<Segment {0}: {1} - {2} ({3})>".format(self.typeof, self.title, self.composer, self.number)

    def show(self, arg=None):
        """Shortcut for music21.stream.show."""

        if not self.score:
            self.make_score()
        self.score.show(arg)

    def xml_write(self, suffix='numbered', path=None):
        """Save a score object in a xml file."""

        if not self.score:
            self.make_score()
        dirname = os.path.dirname(self.filename)
        basename = os.path.basename(self.filename).split('.')[0] + ' - {0}.xml'.format(suffix)
        if path:
            dirname = path
        dest = os.path.join(dirname, basename)
        print "Writing xml file in {0}".format(dest)
        self.score.write('musicxml', dest)

    def make_score(self, number_show=False):
        """Return a score (music21.stream.Stream) object of the
        Segment object."""

        if not self.score:
            newSong = song.makeSong(self.filename, number_show, False)
            newSegment = newSong.getExcerpt(self.initial_event, self.final_event)
            self.score = newSegment
        else:
            print "There is already a score attribute"


def makeSegment(data_input):
    """Return a Segment object from a dictionary with specific data,
    including metadata."""

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
    contour = Contour(score)
    data['ambitus'] = score.analyze("ambitus").chromatic.directed
    data['contour'] = contour
    data['contour_prime'] = contour.reduction_morris()[0]
    data['contour_size'] = len(contour)

    data['typeof'] = data_input['typeof']
    data['number'] = data_input['number']
    data['initial_event'] = initial
    data['final_event'] = final
    data['part_number'] = data_input['part_number']
    data['period_number'] = data_input['period_number']

    return Segment(data)


def formParser(filename):
    """Returns a dictionary with the formal structure of a song
    parsed. The argument is the name of xml file, but the function
    parses the .form file in the same directory of the xml one."""

    form_name = filename.strip('.xml') + '.form'
    with open(form_name, 'r') as f:
        seq = [_utils.remove_endline(el) for el in f.readlines() if _utils.remove_endline(el)]
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


def colorSegmentObj(filename):
    """Return a music21 stream object with colored first and last
    Segment notes."""

    s = song.makeSong(filename, True)
    measures = s.measures
    form = formParser(filename)

    beginning = []
    ending =[]
    for seg in form:
        beginning.append(seg['initial'])
        ending.append(seg['final'])

    n = 0
    for measure in measures:
        events = measure.notesAndRests
        for event in events:
            n += 1
            if n in beginning:
                event.color = 'blue'
            elif n in ending:
                event.color = 'red'

    return s
