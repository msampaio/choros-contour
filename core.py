#!/usr/bin/env python
# -*- coding: utf-8 -*-

import music21
from music21.contour import Contour


class Phrase(object):
    def __init__(self, piece="", number=0, size=0, contour=None, contour_size=0, lily=""):
        self.piece = piece
        self.number = number
        self.size = size
        self.contour = contour
        self.contour_size = contour_size
        self.lily = lily

    def __repr__(self):
        return "<Phrase: {0} {1}:{2}>".format(self.piece, self.number, self.size)


def note_has_fermata(note):
    return any([True for x in note.expressions if isinstance(x, music21.expressions.Fermata)])


def split_phrases(voice):
    phrases = [music21.stream.Stream()]
    counter = 0

    for n in voice.flat.notes.stripTies():
        if n.expressions and note_has_fermata(n):
            phrases[counter].append(n)
            phrases.append(music21.stream.Stream())
            counter += 1
        else:
            phrases[counter].append(n)

    return [phrase for phrase in phrases if phrase]


def make_phrases(filename):
    music = music21.parse(filename)
    piece = music.getElementsByClass(music21.text.TextBox)[0].content
    phrases = split_phrases(music.parts[0])
    result = []
    for number, music in enumerate(phrases):
        contour = Contour(music)
        lily = music.lily
        result.append(Phrase(piece, number, len(music), contour, len(contour), lily))
    return result
