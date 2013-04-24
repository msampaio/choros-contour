#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import music21
import segment
import _utils


class Song(object):
    """Class for song objects."""

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

        if 'subSegments' in data:
            self.subSegments = data['subSegments']
        else:
            self.subSegments = []

    def __repr__(self):
        return "<Song: {0}. {1}>".format(self.title, self.collection)

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

    def addSegment(self, subSegment):
        """Add Segment objects in subSegment attribute."""

        self.subSegments.append(subSegment)
        return self

    def allPhrases(self):
        """Return all the subSegments of type Phrase from the Song
        object."""

        return [un for un in self.subSegments if un.typeof == 'Phrase']

    def showSegment(self, number, typeof='Phrase'):
        """Return a list os all Segment objects from the Song object
        with a given type. Phrase is the default type."""

        return [un for un in self.subSegments if un.typeof == typeof and un.number == number][0]

    # FIXME: rethink the method name
    def showBigSegment(self, number, typeof='Period'):
        """Return a list with all Segment objects of a given big
        segment structures such as Part or Period. The methods
        arguments are the number and type of big structure."""

        if typeof == 'Period':
            return [un for un in self.subSegments if un.period_number == number]
        elif typeof == 'Part':
            return [un for un in self.subSegments if un.part_number == number]
        else:
            print 'Wrong typeof {0}'.format(typeof)

    def getAttr(self, attribute):
        return getattr(self, attribute)

    def setAttr(self, attribute, value):
        setattr(self, attribute, value)
        return self

    def getExcerpt(self, initial, final):
        """Return a score (music21.stream.Stream) object with a
        portion of the Song. The portion includes all numbered music
        events between initial and final values."""

        def make_measure(measure, params, keep_list, n):
            """Returns a music21.stream.Measure object from a given
            measure and list of numbers of the events that will be
            kept in the new object."""

            events = [event for event in measure.notesAndRests if event.event_number in keep_list]
            new_measure = music21.stream.Measure()

            # padding value for small length measures. Pickup measures or not
            events_length = sum((event.quarterLength for event in events))
            measure_length = params['time_signature'].totalLength
            pad = measure_length - events_length

            # tests if measure has pickup
            if measure.notesAndRests[0] != events[0]:
                new_measure.pickup = True
                if pad != 0:
                    new_measure.paddingLeft = pad
            else:
                new_measure.pickup = None

            # insert params only in segment first measure
            if n == 0:
                for values in params.values():
                    new_measure.append(values)

            for event in events:
                new_measure.append(event)

            if pad != 0 and not new_measure.pickup:
                new_measure.paddingRight = pad

            return new_measure

        def make_stream(measures):
            """Return a music21.stream.Stream object with the given
            measures."""

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
        """Return a score (music21.stream.Stream) object of the song
        object."""

        if not self.score:
            newSong = makeSong(self.filename, number_show, False)
            self.params = newSong.params
            self.score = newSong.score
            self.subSegments = newSong.subSegments
            self.measures = newSong.measures
        else:
            print "There is already a score attribute"

def makeSong(filename, number_show=False, save=False):
    """Return a Song object from a xml file. The argument number_show
    means the enumbered numbers will be included in score object, and
    the save argument means the object can be saved in a pickle file,
    that is, the score object will not be included in Song object."""

    def get_parameters(measures):
        """Return a dictionary with clef, key and time parameters of
        the given measures."""

        m1 = measures[0]
        # song data
        params = {}
        params['clef'] = m1.getElementsByClass('Clef')[0]
        params['key_signature'] = m1.getElementsByClass('KeySignature')[0]
        params['time_signature'] = m1.getElementsByClass('TimeSignature')[0]
        return params

    def getSubSegments(filename, songObj, save):
        """Return the Song object with all its Segments in subSegment
        attribute."""

        formname = filename.split('.xml')[0] + '.form'
        if os.path.exists(formname):
            data = segment.formParser(filename)
            for el in data:
                el['filename'] = filename
                el['songObj'] = songObj
                el['save'] = save
                subSegment = segment.makeSegment(el)
                songObj.addSegment(subSegment)
            return songObj
        else:
            print "There is no file {0}".format(formname)
            return songObj

    def pickup_test(measures):
        """Test if the given measures have pickup."""

        if measures[0].number == 0:
            return True

    score = music21.converter.parse(filename)
    part = score.getElementsByClass('Part')[0]
    measures = part.getElementsByClass('Measure')
    params = get_parameters(measures)
    time_signature_obj = params['time_signature']
    key, mode = params['key_signature'].pitchAndMode

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
    data['score'] = score
    data['measures'] = measures
    data['params'] = params

    data['time_signature'] = str(time_signature_obj)
    data['meter'] = time_signature_obj.beatCountName
    data['pickup'] = pickup_test(measures)
    data['key'] = key
    data['mode'] = mode

    newSong = getSubSegments(filename, Song(data), save)

    if save:
        newSong.score = None
        newSong.params = None
        newSong.measures = None
    return  newSong

def makeSongCollection(collection, save=False):
    """Returns a list of phrases objects separated by piece."""

    files = _utils.filenames_list(collection)
    return [makeSong(f, False, save) for f in files]
