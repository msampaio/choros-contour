#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import copy
import shutil
import _utils


def directories(path):
    r = []
    for d in os.listdir(path):
        absolute = os.path.join(path, d)
        if os.path.isdir(absolute):
            r.append(absolute)
    return r

def filename_pattern(pattern, directory):
    def aux(pattern, directory, f):
        return os.path.join(directory, re.search(pattern, f).string)
    
    files = os.listdir(directory)
    return [aux(pattern, directory, f) for f in files if re.search(pattern, f)]


def copy_files(pattern, dirs, dest_dir):

    
    for directory in dirs:
        files = filename_pattern(pattern, directory)
        base_dir = os.path.basename(directory)
        dest = os.path.join(dest_dir, base_dir)
        _utils.mkdir(dest)
        for f in files:
            print "Copying file {0}, of collection {1}...".format(f, base_dir)
            shutil.copy(f, dest)
            

def count_patterns(pattern, directory):
    return [len(filename_pattern(pattern, d)) for d in directory]


if __name__ == '__main__':
    corpus_dir = os.path.expanduser('~/Dropbox/genos-choros/choros-corpus/expandidos')
    dirs = directories(corpus_dir)
    dest_dir = os.path.join(os.getcwd(), 'choros-corpus')
    
    print copy_files('xml$', dirs, dest_dir)
    print copy_files('phrase$', dirs, dest_dir)
