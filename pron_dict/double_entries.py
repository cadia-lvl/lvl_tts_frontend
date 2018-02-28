#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Filter double entries from the lexicon.

"""

import sys

in_file = sys.argv[1]

double_entries = []
previous_word = ''
previous_line = ''
for line in open(in_file).readlines():
    word, pron = line.split('\t')
    if word == previous_word:
        double_entries.append(previous_line.strip())
        double_entries.append(line.strip())

    previous_line = line
    previous_word = word

for line in double_entries:
    print(line)

