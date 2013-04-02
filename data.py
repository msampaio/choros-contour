#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pickle
import phrase


def save_pickle(filename, data):
    with open(os.path.join("data", filename), 'w') as fileobj:
        pickle.dump(data, fileobj)


def load_pickle(filename):
    with open(os.path.join("data", filename)) as fileobj:
        return pickle.load(fileobj)


if __name__ == '__main__':
    pixinguinha = phrase.make_phrase_collection("O Melhor de Pixinguinha", False)
    save_pickle("pixinguinha", pixinguinha)
