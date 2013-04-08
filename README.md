choros-contour
==============

Brazilian choros musical contour analysis

This repository contains the code to analyze musical contour relations
in a large corpus of Brazilian choros using Music21 and
MusiContour.

For more information, http://genosmus.com/pesquisa/contornos/choro/
(in portuguese)

*Corpus limitations*: Our corpus of songs is not available because of
 copyright questions.

# Install

Install [virtualenv](http://genosmus.com/handbook/python/), create a
`choros` environment, activate it and run:

    $ easy_install pip
    $ pip install ipython numpy
    $ pip install matplotlib
    $ pip install -r requirements.txt

Initiate and update submodule

    $ git submodule init
    $ git submodule update

Download `corpus` branch of
[Kroger's Music21 fork](https://github.com/kroger/music21/tree/contour)
and, inside `choros` environment:

    $ python setup.py install

# Use

You must be in `choros` virtualenv environment. Inside it, run ipython

    $ ipython

Then, import `umazero` package

    >>> import umazero

## Create phrases and save them in a variable:

    >>> pixinguinha = umazero.make_phrase_collection("O Melhor de Pixinguinha")

## Save data in a pickle file

    >>> umazero.data.save_pickle('pixinguinha', pixinguinha)

## Load data from a pickle file

    >>> data = umazero.data.load_pickle('pixinguinha')

## Create an object with all phrases to make queries

If the argument is `False`, the data will be loaded from the pickle
files. Default is to create all_phrases.

    >>> phrases = umazero.make_allphrases(False)

## Make queries

It's possible to make several queries from an `AllPhrases` object,
such as by composer, ambitus and Morris reduced contour:

    >>> phrases.byComposer('Pixinguinha')

    >>> phrases.byAmbitus(22)

    >>> from music21.contour import Contour
    >>> phrases.byMorrisReduction(Contour([0, 2, 1]))

## Create pdf file with numbered events

Outside ipython, run:

    $ python song_enumerate.py song.xml

## Create separate xml files for each phrase of a song

A .phrase file of the song must be in the same directory of the song. Outside ipython run:

    $ python phrases_save.py song.xml

*Music21 problem*: It's not possible to save data in pickle, and
 create files for each phrase because of
 [Music21 problem with pickle](https://groups.google.com/forum/?fromgroups=#!topic/music21list/f8hUZqlhc64).
 For while, (un)comment lines in `Phrase` class, and `make_phrase_obj`
 function, in [core.py]() file.

## Create a xml file with colored initial and final notes of phrases

A .phrase file of the song must be in the same directory of the song. Outside ipython run:

    $ python phrases_color.py song.xml
