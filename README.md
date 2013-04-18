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

You must be always in `choros` virtualenv environment to use `umazero`
package.

## Save data from `choros-corpus` directory:

In prompt:

    $ make save_pickle

## Run ipython interpreter and import `umazero` package:

In prompt, run ipython:

    $ ipython

Then, import `umazero` package

    >>> import umazero

## Load and save songs and music units in a variable:

    >>> songs = umazero.loadSongs()
    >>> units = umazero.loadMusicUnits()

## Create song from a xml file:

    >>> umazero.makeSong('file.xml')

## Make queries

It's possible to make several queries from an `AllPhrases` object,
such as by composer, ambitus and Contour Prime Form:

    >>> units = umazero.loadMusicUnits()

    >>> units.byComposer('Pixinguinha')

    >>> units.byAmbitus(22)

    >>> units.byContourPrime(umazero.Contour([0, 2, 1]))

## Create a xml file with numbered events

Outside ipython, run:

    $ python umazero/enumerate_events.py song.xml

## Create a xml file with colored initial and final notes of phrases

A .form file of the song must be in the same directory of the song. Outside ipython run:

    $ python umazero/units_color.py song.xml
