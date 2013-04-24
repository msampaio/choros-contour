#!/usr/bin/env python

import sys
import os
import unit


def colorize(filename):
    """Save a given filename in xml file with 'color' suffix and the
    first and last notes of each MusicUnit colored. The '.form' file
    must be in the same directory of xml file (filename)."""

    print "Precessing song... {0}".format(os.path.basename(filename))
    unit.colorUnitObj(filename).xml_write('color')


if __name__ == '__main__':
    if (len(sys.argv) > 1):
        filenames = sys.argv[1:]
        for f in filenames:
            colorize(f)
    else:
        print "Insert xml filename as argument:\npython enumerate foo.xml"
