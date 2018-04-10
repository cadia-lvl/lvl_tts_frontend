#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

Creates utt2spk from google chitchat text file (line_index.tsv):

input format:

utt_id  e-mail  some-id     utterance

isf_4089_2528110390	chitchat-icelandic-tts-07@sdoperapera.com	00238a4e-c562-4819-b8d6-315d1b17fa18	Þá yrðu fleiri til skiptanna fyrir frænkurnar.


Writes to stdout

"""
import sys
utt2spk = {}

in_file = open(sys.argv[1]) # e.g. TTS_icelandic_Google/isfData/line_index.txt

for line in in_file.readlines():
    utt_id, email, sha, utt = line.split('\t')
    speaker_id = utt_id[4:8]
    utt2spk[utt_id] = speaker_id

for utt in utt2spk.keys():
    print(utt + ' ' + utt2spk[utt])