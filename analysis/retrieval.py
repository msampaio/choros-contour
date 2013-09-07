#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import core
import json
import idcode
import _utils
import copy


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


def getSingleCoreObjFromJson(jsonDic, objClass):
    obj = copy.deepcopy(objClass)
    attribList = obj.__dict__.keys()
    for key, value in jsonDic.items():
        attr = key.split('.')[1]
        if attr in attribList:
            obj.__setattr__(attr, value)
    return obj


def getCoreObjFromJson(jsonFile, objClass):
    jsonSeq = json.load(open(jsonFile))
    return [getSingleCoreObjFromJson(row, objClass) for row in jsonSeq]


def getMusicologicalInfo(jsonDir='json'):

    def pieceAux(pieceDic, composersSeq):
        composerNames = pieceDic['piece.composer']
        composer = [comp for comp in composersSeq if comp.name in composerNames]

        return core.makePiece(pieceDic['piece.title'], composer, pieceDic['piece.year'], pieceDic['piece.city'])

    def sourceAux(sourceDic, collectionsSeq, composersSeq, piecesSeq):
        composerNames = sourceDic['piece.composer']
        collectionTitle = sourceDic['collection.title']
        collectionVolume = sourceDic['collection.volume']
        pieceTitle = sourceDic['piece.title']
        pieceNumber = sourceDic['idcode.pieceNumber']
        composer = [comp for comp in composersSeq if comp.name in composerNames]
        collection = [coll for coll in collectionsSeq if coll.title == collectionTitle and coll.volume == collectionVolume][0]
        collection.makeCollectionCode()
        idCode = idcode.idCodeMaker('T', collection.code, pieceNumber, True, collectionVolume, pieceTitle)
        piece = [pc for pc in piecesSeq if pc.title == pieceTitle and pc.composer == composer][0]

        source = copy.deepcopy(core.Source())
        source.piece = piece
        source.collection = collection
        source.idCode = idCode
        source.filename = os.path.join('corpus', '.'.join([idCode.idCode, 'xml']))
        source.formSeq = None
        source.score = None

        return source

    collections = getCoreObjFromJson(os.path.join(jsonDir, 'collections.json'), core.Collection())
    composers = getCoreObjFromJson(os.path.join(jsonDir, 'composers.json'), core.Composer())

    piecesSeq = json.load(open(os.path.join(jsonDir, 'pieces.json')))
    sourcesSeq = json.load(open(os.path.join(jsonDir, 'sources.json')))
    pieces = [pieceAux(pieceDic, composers) for pieceDic in piecesSeq]
    sources = [sourceAux(sourceDic, collections, composers, pieces) for sourceDic in sourcesSeq]

    return composers, collections, pieces, sources
