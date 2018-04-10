#!/usr/bin/env python

"""
Split an utt2spk file (kaldi ASR format) into enroll and eval directories. From each speaker, three utterances
go into utt2spk file in the enroll directory and the rest goes into the eval directory.
Create the eval and enroll directories beforehand.

Afterwards the other files in the directory (feats.scp, spk2utt, etc.) get fixed with Kaldi's utils/fix_data_dir.sh,
so that all files match (infos missing from one file are deleted from all other files).

Example usage:

kaldi_data_split.py ism_data/utt2spk ism_data/enroll/utt2spk ism_data/eval/utt2spk

"""
import sys,random

dictutt = {}

for line in open(sys.argv[1]):
    line = line.rstrip('\r\t\n ')
    utt, spk = line.split(' ')
    if spk not in dictutt:
        dictutt[spk] = []
    dictutt[spk].append(utt)

fenroll = open(sys.argv[2], 'w')
feval = open(sys.argv[3], 'w')

for key in dictutt:
    utts = dictutt[key]
    random.shuffle(utts)
    for i in range(0, len(utts)):
        line = utts[i] + ' ' + key
        if(i < 3):
            fenroll.write(line + '\n')
        else:
            feval.write(line + '\n')

fenroll.close()
feval.close()
