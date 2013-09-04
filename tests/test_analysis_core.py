# -*- coding: utf-8 -*-

import unittest
import analysis.core as core
import analysis._utils as _utils
import analysis.idcode as idcode


class TestUtils(unittest.TestCase):
    def test_makeCity(self):
        name = 'Salvador'
        province = 'Bahia'
        city = core.City()
        city.name = name
        city.province = province
        self.assertEqual(core.makeCity(name, province), city)
        self.assertNotEqual(core.makeCity('Juazeiro', province), city)

    def test_makeComposer(self):
        completeName = 'Alfredo da Rocha Viana Jr.'
        nickname = 'Pixinguinha'
        gender = 'M'
        bornCityObj = core.makeCity('Rio de Janeiro', 'Rio de Janeiro')
        bornYear = 1897
        deathCityObj = core.makeCity('Rio de Janeiro', 'Rio de Janeiro')
        deathYear = 1973
        mainInstrument = 'Flute'

        composer = core.Composer()
        composer.prename, composer.name = _utils.nameParser(completeName)
        composer.nickname = nickname
        composer.gender = gender
        composer.bornCity = bornCityObj
        composer.bornYear = bornYear
        composer.deathCity = deathCityObj
        composer.deathYear = deathYear
        composer.mainInstrument = mainInstrument
        
        args1 = [completeName, nickname, gender, bornCityObj, bornYear, deathCityObj, deathYear, mainInstrument]
        args2 = [completeName, nickname, 'F', bornCityObj, bornYear, deathCityObj, deathYear, mainInstrument]

        self.assertEqual(core.makeComposer(*args1), composer)
        self.assertNotEqual(core.makeComposer(*args2), composer)


    def test_makePiece(self):
        cityObj = core.makeCity('Rio de Janeiro', 'Rio de Janeiro')
        composerObj = core.makeComposer('Alfredo da Rocha Viana Jr.', 'Pixinguinha')
        title = 'Lamentos'
        subtitle = None
        year = 1928

        piece = core.Piece()
        piece.title = title
        piece.subtitle = subtitle
        piece.composer = [composerObj]
        piece.city = cityObj
        piece.year = year

        args1 = [title, [composerObj], year, subtitle, cityObj]
        args2 = ['Rosa', [composerObj], year, subtitle, cityObj]

        self.assertEqual(core.makePiece(*args1), piece)
        self.assertNotEqual(core.makePiece(*args2), piece)


    def test_makeCollection(self):
        title = 'O melhor do Choro Brasileiro'
        authorList = None
        publisher = 'Irmãos Vitale'
        volume = '1'

        collection = core.Collection()
        collection.title = title
        collection.author = authorList
        collection.publisher = publisher
        collection.volume = volume
        collection.makeCollectionCode()
        
        self.assertEqual(core.makeCollection(title, authorList, publisher, volume), collection) 
        self.assertNotEqual(core.makeCollection(title, authorList, publisher, "2"), collection)

    def test_makeSource(self):
        composerObj = core.makeComposer('Alfredo da Rocha Viana Jr.', 'Pixinguinha')
        collectionObj = core.makeCollection('O melhor do Choro Brasileiro', None, 'Irmãos Vitale', "1")
        pieceObj = core.makePiece('Lamentos', composerObj, 1928)
        filenameOne = '/Users/marcos/Downloads/TOMCB1_34E.xml'
        filenameTwo = '/Users/marcos/Downloads/FOMCB1_34.xml'

        source = core.Source()
        source.piece = pieceObj
        source.collection = collectionObj
        source.filename = filenameOne
        source.idCode = idcode.getIdCodeByFilename(filenameOne)
        
        self.assertEqual(core.makeSource(pieceObj, collectionObj, filenameOne), source)
        self.assertNotEqual(core.makeSource(pieceObj, collectionObj, filenameTwo), source)

if __name__ == '__main__':
    unittest.main()
