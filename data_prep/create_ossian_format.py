#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

Creates Ossian format of text data for TTS, from Festival format.

Festival format:
one text file, content:
( ivona_set1_2113 "hér á landi er erfitt að komast í læri í myndahúðflúr þar sem að fáir stunda þessa grein og markaðurinn lítill hér á landi." )

Ossian format:
one file for each utterance, named after the id:

Filename:   ivona_set1_2113.txt
Content:    hér á landi er erfitt að komast í læri í myndahúðflúr þar sem að fáir stunda þessa grein og markaðurinn lítill hér á landi.


"""

import os
import sys

output_dir = 'ivona_txt'

festival_file = open(sys.argv[1]) # e.g. [..]/ivona/ivona_set1.txt
#os.mkdir(output_dir)

for line in festival_file.readlines():
    quotes_ind = line.index('"')
    if quotes_ind > 20:
        #missing starting quotes in utt
        utt_id = line[2:17]
        text = line[18: quotes_ind]

    else:
        utt_id = line[2:quotes_ind].strip()
        text = line[quotes_ind + 1:line.index('"', quotes_ind + 1)]

    with open(output_dir + '/' + utt_id + '.txt', 'w') as f:
        f.write(text + '\n')

