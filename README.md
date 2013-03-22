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
`choros` environment and, inside it:

    $ easy_install pip
    $ pip install ipython numpy
    $ pip install matplotlib
    $ pip install -r requirements.txt

Download `corpus` branch of
[Kroger's Music21 fork](https://github.com/kroger/music21/tree/contour)
and, inside `choros` environment:

    $ python setup.py install

# Use

You must be in `choros` virtualenv environment. Inside it, run ipython

    $ ipython

## Save phrases in a variable

    >>> import core

    >>> pixinguinha = core.make_phrase_collection("O Melhor de Pixinguinha")

## Save data in a pickle file

    >>> core.save_pickle('pixinguinha', pixinguinha)

## Load data from a pickle file

    >>> data = core.load_pickle('pixinguinha')

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
