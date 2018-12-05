#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Select the entries from an Ossian lexicon that are contained in the frob-formatted input file

"""

import sys

frob_file = sys.argv[1]
out_file = sys.argv[2]

ossian_dict_file = '/Users/anna/Ossian/train/is/components/lexicon-lvldict_sequitur_LTS_ntrain1000_gramlen2_phon2_lett2/lexicon.txt'

ossian_dict = {}

for line in open(ossian_dict_file).readlines():
    entry, pos, transcr = line.split('\t')
    ossian_dict[entry] = transcr.strip()

selected_entries = []

for line in open(frob_file).readlines():
    entry, ipa, sampa, nil = line.split('\t')
    if entry.lower() in ossian_dict:
        selected_entries.append(entry.lower() + '\t' + ossian_dict[entry.lower()])


with open(out_file, 'w') as f:
    for entry in sorted(selected_entries):
        f.write(entry)
        f.write('\n')



