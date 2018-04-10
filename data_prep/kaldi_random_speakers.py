#!/usr/bin/env python

"""
Write a spk2utt file for a given number of speakers from a spk2utt file.

Afterwards the other files in the directory (feats.scp, spk2utt, etc.) get fixed with Kaldi's utils/fix_data_dir.sh,
so that all files match (infos missing from one file are deleted from all other files).

Example usage:

kaldi_data_split.py <input-file> <output-file> <no-of-speakers-to-extract>

kaldi_data_split.py ism_data/utt2spk ism_data/random_speakers/utt2spk 6

"""

import sys,random

input_file = sys.argv[1]
output_file = open(sys.argv[2], 'w')
no_speakers = sys.argv[3]

dictutt = {}

for line in open(input_file):
    line = line.rstrip('\r\t\n ')
    utt, spk = line.split(' ')
    if spk not in dictutt:
      dictutt[spk] = []
    dictutt[spk].append(utt)

cnt = 0
for key in dictutt:
    cnt += 1
    if cnt > no_speakers:
        break
    utts = dictutt[key]
    for i in range(0, len(utts)):
        line = utts[i] + ' ' + key
        output_file.write(line + '\n')

output_file.close()
