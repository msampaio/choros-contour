Tools
=====

core
----

Phrase
......

Class for Phrase objects. It retains music21 stream object, contour
data and metadata such as piece title and composer name.

m21_data
........

Returns Music21 data (flatten stream object, piece name, composer) and
collection from a given xml file path.

phrase_locations_parser
.......................

Returns a list with event numbers of phrases from a `.phrase` file
path.

split_phrase
............

Returns a list of phrases from a given music21 flatten score object,
and a list of phrase locations.


color_phrase_obj
................

Return a music21 stream object with colored first and last phrase
notes.

make_phrase_obj
...............

Returns a list of Phrase objects with each phrase of a given file
path. The file path must not have extension.

filenames_list
..............

Returns a list of paths that have `.phrase`.

make_phrase_collection
......................

Returns a list of phrases objects separated by piece.

save_pickle
...........

Save data in a pickle file.

load_pickle
...........

Load data from a pickle file.

song_enumerate
--------------

parse_music
...........

Return an expanded Music21 score object from a given xml file

count_items
...........

Count events in a Music21 score object

generate_pdf
............

Generate pdf from a xml file with counted events.

phrases_color
-------------

color_run
.........

Generate a xml file with colored notes for first and last note of each
phrase. The input data is the song xml file. The `.phrase` file must
be in the same directory of xml file.
