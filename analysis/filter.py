#!/usr/bin/env python
# -*- coding: utf-8 -*-

import core
import segment


class FilterError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


def getByComposer(objList, composerName):
    """Return a filtered list of objects by a given composer name."""

    def aux(composerName, composerList):
        return any([composerName in obj.name for obj in composerList])

    obj1 = objList[0]
    if type(obj1) == core.Piece:
        return [obj for obj in objList if aux(composerName, obj.composer)]
    elif type(obj1) == core.Source:
        return [obj for obj in objList if aux(composerName, obj.piece.composer)]
    elif type(obj1) == segment.Segment:
        return [obj for obj in objList if aux(composerName, obj.source.piece.composer)]
    else:
        print type(obj1)
        raise FilterError('Wrong object list. Try Piece, Source or Segment')


def getByIdCode(objList, idCodeStr):
    """Return a filtered list of objects by a given composer name."""

    def aux(idCodeStr, obj):
        objIdCode = obj.idCode.idCode

        return objIdCode  == idCodeStr or objIdCode.split('-')[0] == idCodeStr.split('-')[0]

    obj1 = objList[0]
    if type(obj1) == core.Source:
        return [obj for obj in objList if aux(idCodeStr, obj)]
    elif type(obj1) == segment.Segment:
        return [obj for obj in objList if aux(idCodeStr, obj.source)]
    else:
        raise FilterError('Wrong object list. Try Source or Segment')


def getByPieceTitle(objList, pieceTitle):
    """Return a filtered list of objects by a given composer name."""

    def aux(pieceTitle, obj):
        objPieceTitle = obj.title

        return objPieceTitle == pieceTitle or pieceTitle in objPieceTitle

    obj1 = objList[0]
    if type(obj1) == core.Piece:
        return [obj for obj in objList if aux(pieceTitle, obj)]
    elif type(obj1) == core.Source:
        return [obj for obj in objList if aux(pieceTitle, obj.piece)]
    elif type(obj1) == segment.Segment:
        return [obj for obj in objList if aux(pieceTitle, obj.source.piece)]
    else:
        raise FilterError('Wrong object list. Try Piece, Source or Segment')


def getByComposerInstrument(objList, composerInstrument):
    """Return a filtered list of objects by a given composer name."""

    def aux(composerInstrument, composerList):
        return any([composerInstrument in obj.mainInstrument for obj in composerList])

    obj1 = objList[0]
    if type(obj1) == core.Piece:
        return [obj for obj in objList if aux(composerInstrument, obj.composer)]
    elif type(obj1) == core.Source:
        return [obj for obj in objList if aux(composerInstrument, obj.piece.composer)]
    elif type(obj1) == segment.Segment:
        return [obj for obj in objList if aux(composerInstrument, obj.source.piece.composer)]
    else:
        raise FilterError('Wrong object list. Try Piece, Source or Segment')
