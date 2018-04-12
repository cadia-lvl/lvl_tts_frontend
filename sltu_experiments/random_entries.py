#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Select n random entries from a dictionary file

"""

import sys
import random

in_file = open(sys.argv[1])
no_entries = int(sys.argv[2])
out_file = sys.argv[3]

all_entries = in_file.readlines()
random.shuffle(all_entries)
random_entries = all_entries[:no_entries]

with open(out_file, 'w') as f:
    for entry in random_entries:
        f.write(entry)