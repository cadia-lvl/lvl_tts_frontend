#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

Creates Ossian format of text data for TTS, from Festival format.

Festival format:
one text file, content:

( is_is-vmst_91_1-2011-11-14T10:03:40.609633 "Skiptar skoðanir um kvóta." )

Ossian format:
one file for each utterance, named after the id:

Filename:   is_is-vmst_91_1-2011-11-14T10:03:40.609633.txt
Content:    Skiptar skoðanir um kvóta.


"""

import os
import sys

output_dir = 'txt'

festival_file = open(sys.argv[1])
os.mkdir(output_dir)

for line in festival_file.readlines():
    quotes_ind = line.index('"')
    utt_id = line[2:quotes_ind].strip()
    text = line[quotes_ind + 1:line.index('"', quotes_ind + 1)]

    with open(output_dir + '/' + utt_id + '.txt', 'w') as f:
        f.write(text + '\n')

