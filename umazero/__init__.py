# modules
import segment
import song
import retrieval

# classes
from song import Song
from segment import Segment

# functions
from song import makeSong
from song import makeSongAllCollections
from segment import makeSegment
from query import makeAllSegments
from retrieval import loadSongs
from retrieval import loadSegments
from retrieval import saveAll
from songcollections import loadSongCollections
from files import enumerator
from files import colorize
from files import copyfiles
from files import get_collections_names as allCollections

# external
from music21.contour import Contour
