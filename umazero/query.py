#!/usr/bin/env python
# -*- coding: utf-8 -*-

import phrase
import _utils
import data


class AllPhrases(object):
    def __init__(self, songs_phrases, stream):
        self.songs_phrases = songs_phrases
        self.flatten = _utils.flatten(songs_phrases)
        self.songs_number = len(songs_phrases)
        self.phrases_number = len(self.flatten)
        self.stream = stream

    def __repr__(self):
        return "<AllPhrases: {0} songs, {1} phrases. Stream {2}>".format(self.songs_number, self.phrases_number, self.stream)

    def getByComposer(self, composer):
        result = [[phr for phr in song_phrases if phr.composer == composer] for song_phrases in self.songs_phrases]
        return AllPhrases([el for el in result if el], self.stream)

    def getByTitle(self, title):
        result = [[phr for phr in song_phrases if phr.title == title] for song_phrases in self.songs_phrases]
        return AllPhrases([el for el in result if el], self.stream)

    def getByAmbitus(self, ambitus):
        result = [[phr for phr in song_phrases if phr.ambitus == ambitus] for song_phrases in self.songs_phrases]
        return AllPhrases([el for el in result if el], self.stream)

    def getByMorrisReduction(self, morris_reduction_cseg):
        result = [[phr for phr in song_phrases if phr.contour.reduction_morris()[0] == morris_reduction_cseg] for song_phrases in self.songs_phrases]
        return AllPhrases([el for el in result if el], self.stream)


def make_allphrases(stream=True):
    phrases = []
    for coll in _utils.collections_list('choros-corpus'):
        print "Processing collection {0}...".format(coll)
        try:
            if stream:
                coll_data = phrase.make_phrase_collection(coll)
            else:
                coll_data = data.load_pickle(coll)
            phrases.extend(coll_data)
        except:
            print "No .phrase or .xml phrases in collection {0}".format(coll)
    return AllPhrases(phrases, stream)
