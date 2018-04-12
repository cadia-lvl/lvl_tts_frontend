#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Split a datafile after randomizing line order. One file of given size, the other file the rest of the input file.

"""

import sys
import random

in_file = open(sys.argv[1])
no_entries = int(sys.argv[2])
out_file_1 = sys.argv[3]
out_file_2 = sys.argv[4]

all_entries = in_file.readlines()
random.shuffle(all_entries)
random_entries_1 = all_entries[:no_entries]
random_entries_2 = all_entries[no_entries:]

with open(out_file_1, 'w') as f:
    for entry in random_entries_1:
        f.write(entry)

with open(out_file_2, 'w') as f:
    for entry in random_entries_2:
        f.write(entry)