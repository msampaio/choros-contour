#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import copy
import pickle
import _utils
import structure
import idcode
import music
import query


def csvSourcesProcess(filename):
    dirname = os.path.dirname(filename)
    basename = os.path.basename(filename)
    baseprename = os.path.splitext(basename)[0]
    jsonname = os.path.join(dirname, baseprename + '.json')

    _utils.csvToJson(filename)

    oldSeq = json.load(open(jsonname))
    newSeq = []
    for row in oldSeq:
        composers = []
        composers.append(row['piece.composer.one'])
        if row['piece.composer.two'] != '':
            composers.append(row['piece.composer.two'])
        row['piece.composer'] = composers
        del row['piece.composer.one']
        del row['piece.composer.two']

        collectionCode = row['collection.code']
        collectionVolume = row['collection.volume']
        pieceNumber = row['idcode.pieceNumber']
        pieceTitle = row['piece.title']
        idCodeObj = idcode.idCodeMaker('T', collectionCode, pieceNumber, True, collectionVolume, _utils.unicodeNormalize(pieceTitle))
        row['idcode'] = idCodeObj.idCode
        newSeq.append(row)
    with open(jsonname, 'w') as f:
        f.write(json.dumps(newSeq, indent=4))


def csvPiecesProcess(filename):
    dirname = os.path.dirname(filename)
    basename = os.path.basename(filename)
    baseprename = os.path.splitext(basename)[0]
    jsonname = os.path.join(dirname, baseprename + '.json')

    _utils.csvToJson(filename)

    oldSeq = json.load(open(jsonname))
    newSeq = []
    for row in oldSeq:
        composers = []
        composers.append(row['piece.composer.one'])
        if row['piece.composer.two'] != '':
            composers.append(row['piece.composer.two'])
        row['piece.composer'] = composers
        del row['piece.composer.one']
        del row['piece.composer.two']
        newSeq.append(row)
    with open(jsonname, 'w') as f:
        f.write(json.dumps(newSeq, indent=4))


def getSingleStructureObjFromJson(jsonDic, objClass):
    obj = copy.deepcopy(objClass)
    attribList = obj.__dict__.keys()
    for key, value in jsonDic.items():
        attr = key.split('.')[1]
        if attr in attribList:
            obj.__setattr__(attr, value)
    return obj


def getStructureObjFromJson(jsonFile, objClass):
    jsonSeq = json.load(open(jsonFile))
    return [getSingleStructureObjFromJson(row, objClass) for row in jsonSeq]


def getMusicologicalInfo(jsonDir='json'):

    def pieceAux(pieceDic, composersSeq):
        composerNames = pieceDic['piece.composers']
        composers = [comp for comp in composersSeq if comp.name in composerNames]
        return structure.makePiece(pieceDic['piece.title'], composers, pieceDic['piece.year'], pieceDic['piece.city'])

    def sourceAux(sourceDic, collections, composers, pieces):
        composerNames = sourceDic['piece.composers']
        collectionTitle = sourceDic['collection.title']
        collectionVolume = sourceDic['collection.volume']
        pieceTitle = sourceDic['piece.title']
        pieceNumber = sourceDic['idcode.pieceNumber']
        composers = [comp for comp in composers if comp.name in composerNames]
        collection = [coll for coll in collections if coll.title == collectionTitle and coll.volume == collectionVolume][0]
        collection.makeCollectionCode()
        idCode = idcode.idCodeMaker('T', collection.code, pieceNumber, True, collectionVolume, pieceTitle)
        piece = [pc for pc in pieces if pc.title == pieceTitle and pc.composers == composers][0]


        filename = os.path.join('choros-corpus/corpus', '.'.join([idCode.idCode, 'xml']))

        source = structure.makeSource(piece, collection, filename)

        return source

    collections = getStructureObjFromJson(os.path.join(jsonDir, 'collections.json'), structure.Collection())
    composers = getStructureObjFromJson(os.path.join(jsonDir, 'composers.json'), structure.Composer())

    piecesSeq = json.load(open(os.path.join(jsonDir, 'pieces.json')))
    sourcesSeq = json.load(open(os.path.join(jsonDir, 'sources.json')))
    pieces = [pieceAux(pieceDic, composers) for pieceDic in piecesSeq]
    sources = [sourceAux(sourceDic, collections, composers, pieces) for sourceDic in sourcesSeq if sourceDic['collection.title'] != 'Songbook Choro']

    return composers, collections, pieces, sources


def getSegmentsInfo(sourcesObjList):
    return [structure.makeSegments(source, True) for source in sourcesObjList]

def getMusicInfo(jsonDir='json'):
    """Return sequence of objects."""

    composers, collections, pieces, sources = getMusicologicalInfo(jsonDir)
    segments = getSegmentsInfo(sourcesObjList)
    return composers, collections, pieces, sources, segments


def savePickle(data, filename):
    """Save the given data in the filename."""

    _utils.mkdir("data")
    with open(os.path.join("data", filename), 'w') as fileobj:
        print 'Saving in {0}'.format(filename)
        pickle.dump(data, fileobj)


def loadPickle(filename):
    """Load pickle file."""

    with open(os.path.join("data", filename)) as fileobj:
        return pickle.load(fileobj)


def saveAll(partial=False):
    """Save composer, collection, piece and source objects in pickle
    files."""

    for seq in getMusicologicalInfo():
        savePickle(seq, seq[0].__class__.__name__)

    if not partial:
        savePickle(getSegmentsInfo(loadPickle('Source')), 'Segment')


def loadAll(segments=False):
    """Load composer, collection, piece and source objects lists from
    the pickle files saved in data directory."""

    classes = ['Composer', 'Collection', 'Piece', 'Source']
    if segments:
        classes.append('Segment')
    return [loadPickle(f) for f in classes]
