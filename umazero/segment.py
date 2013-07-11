#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import music21
from music21.contour import Contour
from music21.interval import notesToInterval, notesToChromatic
import song
import _utils
import note
import contour


class SegmentException(Exception):
    pass


class Segment(song.Song):
    """Class for Segment classes. A segment is a phrase or link of a
    song."""

    def __init__(self):
        self.filename = None

        # metadata
        self.collection = None
        self.title = None
        self.composers = None
        self.composersStr = None

        # music
        self.score = None
        self.time_signature = None
        self.meter = None
        self.ambitus = None
        self.pickup = None

        self.contour = None
        self.contour_prime = None
        self.contour_size = None

        self.notes = None
        self.intervals = None
        self.intervals_with_direction = None
        self.first_interval = None
        self.last_interval = None

        self.typeof = None
        self.number = None

        self.initial_event = None
        self.final_event = None

        self.part_number = None
        self.period_number = None

    def __repr__(self):
        return "<Segment {0}: {1} - {2} ({3})>".format(self.typeof, self.title, self.composersStr, self.number)

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
        self.score.metadata.movementNumber = 'Segment {0}'.format(self.number)


    def midi_save(self, path=None):
        """Save score as midi file in a given path."""

        if not self.score:
            self.make_score()

        if path == None:
            basename = os.path.basename(self.filename)
            dirname = os.path.dirname(self.filename)
            midiname = " - ".join([basename.split('.')[0], self.typeof, str(self.number)]) + '.mid'
            path = os.path.join(dirname, midiname)

        print "Saving object {0} as midi file in path {1}".format(self, path)
        mf = music21.midi.translate.streamToMidiFile(self.score)
        mf.open(path, 'wb')
        mf.write()
        mf.close()


def makeSegment(segment_form):
    """Return a Segment object from a dictionary with specific data
    about the segment, including metadata."""

    seg = Segment()
    initial = segment_form['initial']
    final = segment_form['final']

    songObj = segment_form['songObj']
    score = songObj.getExcerpt(initial, final)
    
    seg.filename = songObj.filename

    # metadata
    seg.collection = songObj.collection
    seg.title = songObj.title
    seg.composers = songObj.composers
    seg.composersStr = songObj.composersStr

    # music
    if not segment_form['save']:
        seg.score = score

    seg.time_signature = songObj.time_signature
    seg.meter = songObj.meter
    seg.pickup = score.pickup

    # analysis
    contourObj = Contour(score)
    seg.ambitus = score.analyze("ambitus").chromatic.directed
    seg.contour = contourObj
    # FIXME: the reduction_morris method in wrong in Music21. Using local Sampaio prime form
    seg.contour_prime = contour.sampaio(contourObj.reduction_morris()[0])
    seg.contour_size = len(contourObj)

    notes = note.song_notes(score)
    seg.notes = [note.make_note(n) for n in notes]
    _size = len(notes)

    seg.intervals = note.intervals_without_direction(notes)
    seg.intervals_with_direction = note.intervals_with_direction(notes)
    seg.intervals_with_direction_semitones = note.intervals_with_direction_semitones(notes)
    seg.first_interval = notesToChromatic(notes[0], notes[1]).directed
    seg.last_interval = notesToChromatic(notes[_size - 2], notes[_size - 1]).directed

    seg.typeof = segment_form['typeof']
    seg.number = segment_form['number']
    seg.initial_event = initial
    seg.final_event = final
    seg.part_number = segment_form['part_number']
    seg.period_number = segment_form['period_number']
    seg.segment_number = segment_form['segment_number']

    return seg


# FIXME: period enumeration when a subsequent part doesn't contain a
# period.
def formParser(filename):
    """Returns a dictionary with the formal structure of a song
    parsed. The argument is the name of xml file, but the function
    parses the .form file in the same directory of the xml one."""

    form_name = filename.replace('.xml', '.form')
    with open(form_name, 'r') as f:
        lines = f.readlines()
        seq = []
        for el in lines:
            seq_el = _utils.remove_endline(el).strip(' ')
            if seq_el not in [' ', '']:
                seq.append(seq_el)
    form = []
    part_number = 0
    period_number = 0
    phrase_number = 0
    link_number = 0
    segment_number = 0

    for el in seq:
        if el == '# part':
            part_number += 1
            period_number = 0
        elif el == '# period':
            period_number += 1
        else:
            typeof, i, f = el.split()
            initial = int(i)
            final = int(f)
            segment_number += 1

            segment_form = {}
            segment_form['initial'] = initial
            segment_form['final'] = final
            segment_form['period_number'] = period_number
            segment_form['part_number'] = part_number
            segment_form['segment_number'] = segment_number

            if typeof == 'p':
                phrase_number += 1
                segment_form['typeof'] = 'Phrase'
                segment_form['number'] = phrase_number
            else:
                link_number += 1
                segment_form['typeof'] = 'Link'
                segment_form['number'] = link_number
            form.append(segment_form)

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
