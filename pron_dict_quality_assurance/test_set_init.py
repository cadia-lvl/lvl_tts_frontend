#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Extract transcripts for words in test set, if they are included in a transcribed dictionary.

Write out entry with transcript if found, otherwise write the entry without transcript. Keep the order of the test set.
"""

import sys

pron_dict_in = open(sys.argv[1])
test_set_in = open(sys.argv[2])

pron_dict = {}

for line in pron_dict_in.readlines():
    word, transcr = line.strip().split('\t')
    pron_dict[word] = transcr

counter = 0
for line in test_set_in.readlines():
    if line.strip() in pron_dict:
        print(line.strip() + '\t' + pron_dict[line.strip()])
        counter += 1
    else:
        print(line.strip())

print('Found transcripts for ' + str(counter) + ' entries')