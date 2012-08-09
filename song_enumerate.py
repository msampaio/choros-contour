#!/usr/bin/env python

import os
import sys
import music21

def parse_music(filename):
    score = music21.parse(filename)
    try:
        score = score.expandRepeats()
    except music21.repeat.ExpanderException:
        print "Warning: can't expand repetitions.", score

    return score


def count_items(score):
    notes = score.parts[0].flat.notesAndRests
    for x, note in enumerate(notes, 1):
        if x % 5 == 0:
            note.addLyric(x)


def generate_pdf(filename):
    # If we use a file with spaces we'll have problems
    basename = os.path.splitext(filename)[0].replace(" ", "-")
    score = parse_music(filename)
    count_items(score)
    lily = music21.lily.translate.LilypondConverter()
    lily.loadObjectFromScore(score)
    lily.createPDF(basename)
    # Music21 leaves the lilypond file behind. Let's delete it.
    os.remove(basename)

if __name__ == '__main__':
    if (len(sys.argv) > 1):
        filenames = sys.argv[1:]
        for f in filenames:
            generate_pdf(f)
    else:
        print "Insert xml filename as argument:\npython enumerate foo.xml"
