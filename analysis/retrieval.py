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


def getSingleStructureObjFromJson(jsonDic, objClass, idn):
    obj = copy.deepcopy(objClass)
    attribList = obj.__dict__.keys()
    obj.__setattr__('idn', idn)
    for key, value in jsonDic.items():
        attr = key.split('.')[1]
        if attr in attribList:
            obj.__setattr__(attr, value)
    return obj


def getStructureObjFromJson(jsonFile, objClass):
    jsonSeq = json.load(open(jsonFile))
    return [getSingleStructureObjFromJson(row, objClass, idn) for idn, row in enumerate(jsonSeq)]


def getMusicologicalInfo(jsonDir='json'):

    def pieceAux(pieceDic, composersSeq, idn):
        composerNames = pieceDic['piece.composers']
        composers = [comp for comp in composersSeq if comp.name in composerNames]
        return structure.makePiece(pieceDic['piece.title'], composers, pieceDic['piece.year'], pieceDic['piece.city'], idn)

    def sourceAux(sourceDic, collections, composers, pieces, idn):
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

        source = structure.makeSource(piece, collection, filename, False, idn)

        return source

    collections = getStructureObjFromJson(os.path.join(jsonDir, 'collections.json'), structure.Collection())
    composers = getStructureObjFromJson(os.path.join(jsonDir, 'composers.json'), structure.Composer())

    piecesSeq = json.load(open(os.path.join(jsonDir, 'pieces.json')))
    sourcesSeq = json.load(open(os.path.join(jsonDir, 'sources.json')))
    pieces = [pieceAux(pieceDic, composers, idn) for idn, pieceDic in enumerate(piecesSeq)]
    sources = [sourceAux(sourceDic, collections, composers, pieces, idn) for idn, sourceDic in enumerate(sourcesSeq) if sourceDic['collection.title'] != 'Songbook Choro']

    return composers, collections, pieces, sources


def getSegmentsInfo(sourcesObjList):
    return [structure.makeSegments(source, True) for source in sourcesObjList]

def getMusicInfo(jsonDir='json'):
    """Return sequence of objects."""

    composers, collections, pieces, sources = getMusicologicalInfo(jsonDir)
    segments = getSegmentsInfo(sourcesObjList)
    return composers, collections, pieces, sources, segments


def singleSavePickle(obj):
    """Save the given object in its corresponding filename."""

    idn = str(obj.idn)
    structureType = obj.__class__.__name__
    path = os.path.join("data", structureType)
    _utils.mkdir("data")
    _utils.mkdir(path)
    with open(os.path.join(path, str(idn)), 'w') as fileobj:
        pickle.dump(obj, fileobj)


def savePickle(objects):
    """Save the given objects sequence in their corresponding
    filename."""

    print 'Saving {0}: {1} objects'.format(objects[0].__class__.__name__, len(objects))
    for obj in objects:
        singleSavePickle(obj)
        obj = None


def singleLoadPickle(structureType, objIdn):
    """Loads the object with the given structure type and idn."""

    path = os.path.join('data', structureType, str(objIdn))
    with open(path, 'r') as fileobj:
        return pickle.load(fileobj)


def loadPickle(structureType):
    """Save the given objects sequence in their corresponding
    filename."""

    path = os.path.join('data', structureType)
    files = os.listdir(path)
    if '.DS_Store' in files:
        files.remove('.DS_Store')
    print 'Loading {0}'.format(structureType)
    return [singleLoadPickle(structureType, idn) for idn in files]


def makeAndSaveSegmentPickle(source, idn):
    sourceScore = copy.deepcopy(source.score)
    for formStructure in source.form.sequence:
        seg = structure.makeSegment(source, formStructure, True, idn)
        idn += 1
        singleSavePickle(seg)
        source.score = copy.deepcopy(sourceScore)
    return idn


def saveSegments(pointer=None):
    sources = sorted(loadPickle('Source'))
    idn = 0

    if pointer:
        idn = sum([src.form.length for src in sources[:pointer[0]]])
        sources = sources[pointer[0]:pointer[1]]

    for source in sources:
        if not source.score:
            source.makeScore()
        source = music.getInfoAboutSource(source)
        idn = makeAndSaveSegmentPickle(source, idn)


def saveAll(segments=False):
    """Save composer, collection, piece, source, and, optionally,
    segments in pickle files."""

    for seq in getMusicologicalInfo():
        savePickle(seq)
    if segments:
        saveSegments()


def loadAll(segments=False):
    """Load composer, collection, piece and source objects lists from
    the pickle files saved in data directory."""

    classes = ['Composer', 'Collection', 'Piece', 'Source']
    if segments:
        classes.append('Segment')
    return [loadPickle(f) for f in classes]


def loadToQuery(structureType='Segment'):
    """Return a Query object with the given structure type saved in
    pickle files."""

    return query.makeQuery(loadPickle(structureType))
