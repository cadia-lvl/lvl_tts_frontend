#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Remove words from a word list from a dictionary.
Write out a new dictionary.

input format dictionary:

word    t r a n s c r i p t i o n
...



"""

import sys

frob_file = sys.argv[1]
word_list_file = sys.argv[2]

word_list = []

for line in open(word_list_file).readlines():
    word_list.append(line.strip().lower())

result_dictionary = []

for line in open(frob_file):
    word, transcr = line.strip().split('\t')
    if word.lower() not in word_list:
        result_dictionary.append(line)

with open(frob_file + '_filtered.txt', 'w') as f:
    for item in result_dictionary:
        f.write(item)