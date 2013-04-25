choros-contour
==============

Brazilian choros musical contour analysis

This repository contains the code to analyze musical contour relations
in a large corpus of Brazilian choros using Music21 and MusiContour.
The data visualization is available at http://umazero.genosmus.com

For more information about the project, see
http://genosmus.com/pesquisa/contornos/choro/ (in portuguese)

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

    $ make save

## Run ipython interpreter and import `umazero` package:

In prompt, run ipython:

    $ ipython

Then, import `umazero` package

    >>> import umazero

## Load and save songs and segments in a variable:

    >>> songs = umazero.loadSongs()
    >>> segments = umazero.loadSegments()

## Create song from a xml file:

    >>> umazero.makeSong('file.xml')

## Make queries

It's possible to make several queries from an `AllSegments` object,
such as by composer, ambitus and Contour Prime Form:

    >>> segments = umazero.loadSegments()

    >>> segments.byComposer('Pixinguinha')

    >>> segments.byAmbitus(22)

    >>> segments.byContourPrime(umazero.Contour([0, 2, 1]))

It's also possible to list all composers, ambitus and contour prime
forms:

    >>> segments.allComposers()
    
    >>> segments.allAmbitus()
    
    >>> segments.allContourPrime()

## Create a xml file with numbered events


    >>> umazero.enumerator('song.xml')

It's possible to enumerate an entire collection of songs:

    >>> umazero.enumerator('/tmp/collection')

It's also possible to enumerate all collections of songs:

    >>> umazero.enumerator('choros-corpus')

## Create a xml file with colored initial and final notes of phrases

A .form file of the song must be in the same directory of the song.

    >>> umazero.colorize('song.xml')
