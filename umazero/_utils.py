#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import os
import glob
import unicodedata
from PIL import Image, ImageChops
from collections import Counter
import query


def flatten(seq):
    """Flatten Sequences.

    >>> flatten([[0, 1], [2, 3]])
    [0, 1, 2, 3]
    """

    return [item for sublist in seq for item in sublist]


def sort2(dic):
    """Return a sorted sequence from a dictionary organized by the dictionary values."""

    return sorted(dic.items(), reverse=True, key=lambda x: x[1])


def percentual(seq):
    """Return a sequence with percentual values."""

    total = sum(seq)
    return [(el * 100 / float(total)) for el in seq]


def percentage(dic):
    """Return a dictionary with percent values"""

    def perc(val, total):
        return val * 100.0 / total

    total = sum(dic.values())
    return {k: perc(v, total) for k, v in dic.items()}


def subplot_base(plots_number):
    maximum = 3
    square = plots_number ** 0.5
    rows_columns = math.ceil(square)
    return int((rows_columns - 1) * 100 + rows_columns * 10)


def filenames_list(collection, extension='form'):
    """Returns a list of paths that have .form."""

    directory = os.path.join(os.getcwd(), 'choros-corpus', collection)
    phrase_files = glob.glob(os.path.join(directory, "*.{0}".format(extension)))

    return [filename.replace(extension, 'xml') for filename in phrase_files]


def filename_exclusion(path, exclusions=['.DS_Store', '.git', 'README.md']):
    """Return a sequence of files from a path without the files given
    in exclusions sequence."""

    files = os.listdir(path)
    for ex in exclusions:
        if ex in files:
            files.remove(ex)
    return files


def mkdir(path):
    """Make a path of a given path, if it doesn't exist."""

    if not os.path.exists(path):
        os.mkdir(path)


def unicode_normalize(string):
    """Return a normalized string. It's useful to process filenames
    with special characters."""

    new_string = unicodedata.normalize('NFKD', unicode(string)).encode('ascii', 'ignore')
    return new_string.replace(',', '').replace('?', '').replace('(', '').replace(')', '')


def group_minorities(dic, percentage=0.05):
    """Return a given dictionary of values, such as {'a': 2, 'b': 4}
    with the keys with the smallest values grouped as 'Others' key.
    The percentage argument defines how small these values must be to
    be grouped."""

    total = sum(dic.viewvalues())
    smallest = total * percentage
    minors = 0
    for k, v in dic.items():
        if v <= smallest:
            minors += v
            dic.pop(k)
    if minors != 0:
        dic['Others'] = minors
    return dic


def image_trim(filename):
    """Save a given image cropped and trimmed. It's useful to remove
    Lilypond tagline and to eliminate blank paper area from the
    image."""

    im = Image.open(filename)
    im = im.crop((0, 0, 776, 1000))
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    bbox = diff.getbbox()
    if bbox:
        im = im.crop(bbox)
        im.save(filename)


def remove_endline(string):
    """Return a given string without new line or crlf."""

    return string.replace('\n', '').replace('\r', '')


def get_filename(collection_number, song_number, path='choros-corpus'):
    """Return absolute filename of a given collection and song numbers."""

    collection = filename_exclusion(path)[collection_number]
    print collection
    files = filenames_list(collection, 'xml')
    for f in files:
        basename = os.path.basename(f)
        number = int(basename.split()[0])
        if number == song_number:
            return f


def count_segments(AllSegmentsObj, attrib):
    return Counter((getattr(seg, attrib) for seg in AllSegmentsObj.segments))


def dicValueInsertion(dic, key, value):
    """Return a given value only if it's not the key value of a given
    dictionary."""

    if key in dic:
        return dic[key]
    else:
        return value


def makeAttribCoordSequence(AllSegmentsObj, attrib, topComposers):
    def aux(AllSegmentsObj, attrib, composer):
        if composer == 'All composers':
            counted = count_segments(AllSegmentsObj, attrib)
        else:
            counted = count_segments(AllSegmentsObj.getByComposer(composer), attrib)
        return [counted.values(), counted.keys()]

    allAndTopComposers = flatten([['All composers'], topComposers])

    return [aux(AllSegmentsObj, attrib, composer) for composer in allAndTopComposers]


def minoritiesRemotion(matrix, valuesCategories, valuesNumber):
    size = len(matrix)
    if size ==  valuesNumber:
        return matrix, valuesCategories
    else:
        valuesAndMatrix = zip(valuesCategories, [sum(els) for els in matrix], matrix)
        sortedValuesAndMatrix = sorted(valuesAndMatrix, reverse=True, key=lambda x:x[1])
        mostCommon = sortedValuesAndMatrix[:valuesNumber]
        other = tuple([sum(els) for els in zip(*[x[2] for x in sortedValuesAndMatrix[valuesNumber:]])])
        mostCommon.insert(0, ('Other', sum(other), other))

        newValuesCategories = []
        newMatrix = []

        for avalue, amount, amatrix in mostCommon:
            newValuesCategories.append(avalue)
            newMatrix.append(amatrix)

        return newMatrix, newValuesCategories


def appendMatrix(matrix, values, valuesCategories):
    """Insert a row of values in a given matrix

    >>> appendMatrix([], [True, True, False], ['True', 'False'])
    [[33.333333333333336, 66.66666666666667, 0, 0]]
    """

    # values in percentage
    counted = percentage(Counter(values))
    composerValuesCategories = counted.keys()

    for valueCategory in valuesCategories:
        if valueCategory not in composerValuesCategories:
            counted[valueCategory] = 0

    categoryAndValueSeq = sorted(counted.items())
    matrix.append([value for category, value in categoryAndValueSeq])

    return matrix


def makeAttribValuesSequence(allSegmentObj, composer, attrib):
    """Return a sequence of attribute values from a given composer and
    attribute.

    # allseg is a query.AllSegments object

    >>> makeAttribValuesSequence(allseg, 'Pixinguinha', 'meter')
    [Duple', 'Duple', 'Triple', ... , 'Duple', 'Duple']
    """

    composerSegmentsSeq = allSegmentObj.getByComposer(composer).segments

    if attrib in ('contour', 'contour_prime'):
        values = [tuple(getattr(seg, attrib)) for seg in composerSegmentsSeq]
    else:
        values = [getattr(seg, attrib) for seg in composerSegmentsSeq]

    return values


def appendAttribMatrix(matrix, allSegmentObj, composer, attrib, valuesCategories):
    """Make a sequence of attribute values and append it to a given matrix

    # allseg is a query.AllSegments object

    >>> appendAttribMatrix([], allseg, 'Pixinguinha', 'pickup', ['True', 'False'])
    [[25.617977528089888, 74.38202247191012, 0, 0]]
    """

    values = makeAttribValuesSequence(allSegmentObj, composer, attrib)

    return appendMatrix(matrix, values, valuesCategories)


def makeAttribValuesMatrix(allSegmentObj, attrib, allAndTopComposers):
    """Return a matrix with data to plot in stackedBar chart, and a
    sequence with the values categories.

    >>> makeAttribValuesMatrix(allseg, 'meter', ['All composers', u'Benedito Lacerda', u'Ernesto Nazareth'])

    ([[97.2508591065292, 0.9163802978235968, 1.8327605956471935], [100.0, 0, 0], [100.0, 0, 0]],
    ['Duple', 'Quadruple', 'Triple'])
    """

    matrix = []
    valuesCategories = query.getData(allSegmentObj.segments, attrib)

    if attrib in ('contour', 'contour_prime'):
        valuesCategories = [tuple(cseg) for cseg in valuesCategories]

    for composer in allAndTopComposers:
        matrix = appendAttribMatrix(matrix, allSegmentObj, composer, attrib, valuesCategories)

    return matrix, valuesCategories


def makeMatrix(matrix, allAndTopComposers, valuesCategories, valuesNumber, contourType=False):
    """Transpose a given matrix and return also a sequence of values
    categories and all and top composers.

    >>> matrix = [[97.2508591065292, 0.9163802978235968, 1.8327605956471935],
                  [100.0, 0, 0],
                  [100.0, 0, 0]]
    >>> allAndTopComposers = ['All composers', u'Benedito Lacerda', u'Ernesto Nazareth']
    >>> makeMatrix(matrix, ['Duple', 'Quadruple', 'Triple'], 3, False)
    ([(97.2508591065292, 100.0, 100.0), (0.9163802978235968, 0, 0), (1.8327605956471935, 0, 0)],
    ['Duple', 'Quadruple', 'Triple'],
    ['All composers', u'Benedito Lacerda', u'Ernesto Nazareth'])
    """

    size = len(matrix)
    transposedMatrix = zip(*matrix)

    newMatrix, newValuesCategories = minoritiesRemotion(transposedMatrix, valuesCategories, valuesNumber)

    if contourType:
        from music21.contour.contour import Contour
        newValuesCategories = flatten([[val[0]], [Contour(cseg) for cseg in val[1:]]])

    return newMatrix, newValuesCategories, allAndTopComposers


def attribValuesMatrix(allSegmentObj, topComposers, attrib, valuesNumber=5):
    """Return a Sequence with a Matrix of attribute values, all
    attribute values and top composers."""

    allAndTopComposers = flatten([['All composers'], topComposers])
    attribMatrix, valuesCategories = makeAttribValuesMatrix(allSegmentObj, attrib, allAndTopComposers)

    return makeMatrix(attribMatrix, allAndTopComposers, valuesCategories, valuesNumber)
