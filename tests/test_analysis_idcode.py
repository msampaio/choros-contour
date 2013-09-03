# -*- coding: utf-8 -*-

import unittest
import analysis.idcode as idcode


class TestUtils(unittest.TestCase):
    def test_idCodeMaker(self):
        idCodeObj = idcode.IdCode()
        idCodeObj.type = 'T'
        idCodeObj.collectionCode = 'MCB'
        idCodeObj.collectionVolume = '1'
        idCodeObj.pieceNumber = '34'
        idCodeObj.expansion = True
        idCodeObj.pieceTitle = 'Lamentos'
        idCodeObj.idCode = 'TMCB1_34E-Lamentos'

        self.assertEqual(idcode.idCodeMaker('T', 'MCB', '34', True, '1', 'Lamentos'), idCodeObj)

    def test_idCodeParser(self):
        self.assertEqual(idcode.idCodeParser('FMP_01'), idcode.idCodeMaker('F', 'MP', '01'))
        self.assertEqual(idcode.idCodeParser('TMP_01E'), idcode.idCodeMaker('T', 'MP', '01', True))
        self.assertEqual(idcode.idCodeParser('FMCB1_34'), idcode.idCodeMaker('F', 'MCB', '34', False, '1'))
        self.assertEqual(idcode.idCodeParser('TMCB1_34E'), idcode.idCodeMaker('T', 'MCB', '34', True, '1'))
        self.assertEqual(idcode.idCodeParser('TMCB1_34E-Lamentos'), idcode.idCodeMaker('T', 'MCB', '34', True, '1', 'Lamentos'))
        self.assertEqual(idcode.idCodeParser('TMCB1_34-Lamentos'), idcode.idCodeMaker('T', 'MCB', '34', False, '1', 'Lamentos'))

