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
and, inside new environment:

    $ python setup.py install

# Use

You must be in choros virtualenv environment. Inside it, run ipython

    $ ipython

## Save phrases in a variable

    \>\>\> import core

    \>\>\> pixinguinha = core.make_phrase_collection("O Melhor de Pixinguinha")

## Save data in a pickle file

    \>\>\> core.save_pickle('pixinguinha', pixinguinha)

## Load data from a pickle file

    \>\>\> data = core.load_pickle('pixinguinha')

## Create pdf file with numbered events

Outside ipython, run:

    $ python song_enumerate.py song.xml
