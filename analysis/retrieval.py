#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import core
import json
import idcode
import _utils


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
