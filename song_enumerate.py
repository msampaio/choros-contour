#!/usr/bin/env python

import os
import sys
import shutil
import _utils
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

    # copy files to temporary directory and rename files
    tmpdir = '/tmp/choros'
    _utils.mkdir(tmpdir)
    dirname = os.path.dirname(filename)
    basename = os.path.basename(filename)
    shutil.copy(filename, tmpdir)
    tmpname = os.path.join(tmpdir, basename)
    nospacename = os.path.splitext(tmpname)[0].replace(" ", "-")

    # count items and generate pdf
    score = parse_music(filename)
    count_items(score)
    lily = music21.lily.translate.LilypondConverter()
    lily.loadObjectFromScore(score)
    lily.createPDF(nospacename)

    # rename and move to original directory
    new_name = os.path.join(tmpdir, basename.split('.')[0] + '.pdf')
    old_name = nospacename + ".pdf"
    os.rename(old_name, new_name)
    shutil.copy(new_name, dirname)

    # Music21 leaves the lilypond file behind. Let's delete it.
    for f in tmpname, new_name, nospacename:
        os.remove(f)

if __name__ == '__main__':
    if (len(sys.argv) > 1):
        filenames = sys.argv[1:]
        for f in filenames:
            generate_pdf(f)
    else:
        print "Insert xml filename as argument:\npython enumerate foo.xml"
