#!/usr/bin/env python

import os
import sys
import phrase


def color_run(filename):
    print "Precessing song... {0}".format(os.path.basename(filename))
    basename = filename.split('.')[0]
    phrase.color_phrase_obj(basename).write('musicxml', basename + ' - color.xml')

    
if __name__ == '__main__':
    if (len(sys.argv) > 1):
        filenames = sys.argv[1:]
        for f in filenames:
            color_run(f)
    else:
        print "Insert xml filename as argument:\npython enumerate foo.xml"
