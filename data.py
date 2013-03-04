#!/usr/bin/env python
# -*- coding: utf-8 -*-

import core


if __name__ == '__main__':
    pixinguinha = core.make_phrase_collection("O Melhor de Pixinguinha")
    core.save_pickle("pixinguinha", pixinguinha)
