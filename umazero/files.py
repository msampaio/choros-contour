#!/usr/bin/env python

import os
import re
import copy
import shutil

import song
import segment
import _utils


def enumerator(path):
    """Save xml files with enumerated events. The path argument can be
    a single xml file, a directory with xml files, or a directory of
    directories (collections) of xml files."""

    if os.path.isfile(path):
        save(path)
    else:
        songs = [x for x in get_songs(path)]
        if not songs:
            songs = get_songs_filenames(path)
        for f in songs:
            save(f)


def colorize(filename):
    """Save a given filename in xml file with 'color' suffix and the
    first and last notes of each Segment colored. The '.form' file
    must be in the same directory of xml file (filename)."""

    print "Precessing song... {0}".format(os.path.basename(filename))
    segment.colorSegmentObj(filename).xml_write('color')


def directories(path):
    """Return a sequence of subdirectories in a complete form of a
    given path."""

    r = []
    for d in os.listdir(path):
        absolute = os.path.join(path, d)
        if os.path.isdir(absolute):
            r.append(absolute)
    return r

def filename_pattern(pattern, directory):
    """Return a sequence of all files of a given directory with
    filenames matching with a given regular expression."""

    def aux(pattern, directory, f):
        return os.path.join(directory, re.search(pattern, f).string)
    
    files = os.listdir(directory)
    return [aux(pattern, directory, f) for f in files if re.search(pattern, f)]


def copy_files(pattern, dirs, dest_dir):
    """Copy files with filenames matching with a given regular
    expression from a dirs directory for a dest_dir directory."""

    for directory in dirs:
        files = filename_pattern(pattern, directory)
        base_dir = os.path.basename(directory)
        dest = os.path.join(dest_dir, base_dir)
        _utils.mkdir(dest)
        for f in files:
            print "Copying file {0}, of collection {1}...".format(f, base_dir)
            shutil.copy(f, dest)


def get_songs(path, pattern='^((?!numbered).)*\.xml$'):
    """Return a generator object with songs of a given path that
    filename matches with the given regular expression pattern."""

    files = os.listdir(path)
    songs = (os.path.join(path, re.search(pattern, f).string) for f in files if re.search(pattern, f))
    return songs


def get_collections_names(collections_dir='choros-corpus'):
    """Return a sequence with collections names from a given
    collections directory."""

    exclusions = ['.DS_Store', '.git', 'README.md', '.gitignore']
    return _utils.filename_exclusion(collections_dir, exclusions)


def get_songs_filenames(collections_dir, suffix='xml'):
    """Return a sequence of song filenames from a given
    collections_dir path, which song filenames match with a regular
    expression pattern, and are not in exclusions sequence."""

    collections = get_collections_names(collections_dir)
    pattern = '^((?!numbered).)*\.{0}$'.format(suffix)

    result = []
    for collection in collections:
        songs = get_songs(os.path.join(collections_dir, collection), pattern)
        result.extend(songs)

    return result


def save(filename):
    """Save a given xml file with numbered events in a new filename
    with 'numbered' suffix."""

    print ". Processing {0}...".format(filename)
    s = song.makeSong(filename, True)
    s.xml_write('numbered')


def copyfiles(path='~/Dropbox/genos-choros/choros-corpus/expandidos'):
    """Copy all files from a given path to 'choros-corpus' repository
    path."""

    corpus_dir = os.path.expanduser(path)
    dirs = directories(corpus_dir)
    dest_dir = os.path.join(os.getcwd(), 'choros-corpus')

    pattern = '^((?!numbered).)*\.(form|xml)$'
    copy_files(pattern, dirs, dest_dir)


def formCheckerFile(formFile):
    def checkPeriods(formFile, errorSeq):
        def aux(dic):
            return dic['part_number'], dic['period_number'], dic['segment_number']

        xmlFile = formFile.replace('.form', '.xml')
        dicSeq = segment.formParser(xmlFile)
        tuples = [aux(dic) for dic in dicSeq]
        for tup in _utils.splitTupleSequence(tuples, 1):
            if len(tup) < 2:
                errorSeq.append([0, 'There is a period with less than two phrases'])


    def checkNumbers(n, string, sequence, errorSeq):
        eventNumbers = string.replace('p ', '').replace('l ', '').split(' ')[:2]
        numbersSize = len(eventNumbers)
        if numbersSize == 2:
            for eventNumber in eventNumbers:
                intEventNumber = int(eventNumber)
                if len(sequence) > 0:
                    last = sequence[-1]
                    if intEventNumber < last:
                        errorSeq.append([n, string])
                sequence.append(intEventNumber)
        else:
            errorSeq.append([n, 'Error in p/l lines'])
            sequence.append(eventNumbers)

    with open(formFile, 'r') as f:
        lines = f.readlines()
        error = []
        events = []
        for n, line in enumerate(lines):
            newLine = _utils.remove_endline(line).rstrip(' ').replace('  ', ' ')
            regexObj = re.search('^[lp] [0-9]', newLine)
            if regexObj:
                checkNumbers(n, regexObj.string, events, error)
            elif newLine in ['', '# part', '# period']:
                pass
            else:
                error.append([n, line])

        if 'Error in p/l lines' not in _utils.flatten(error):
            checkPeriods(formFile, error)

        if len(error) > 0:
            print 'Error in file {0}'.format(formFile)
            for l in error:
                print '{0}: {1}'.format(*l)

def formChecker(directory='choros-corpus'):
    allFiles = get_songs_filenames(directory, 'form')
    for f in allFiles:
        formCheckerFile(f)
