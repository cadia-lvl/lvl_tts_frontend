#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Filter the original Frob by the entries contained in the corpus based lexicon from the ASR system, now used
in the TTS system.

Collect the entries not contained in the TTS version.

Create a tab-separated version of the Frob entries, they are comma-separated in the input

"""

import sys

frob_file = sys.argv[1]
tts_lex_file = sys.argv[2]

tts_lex = []

for line in open(tts_lex_file).readlines():
    word, pos, transcr = line.split('\t')
    tts_lex.append(word)

in_tts_lex = []
not_in_tts_lex = []

abbr = []

for line in open(frob_file):
    arr = line.split(',')
    # the file contains a reference line we don't want
    if len(arr) != 4:
        print(arr)
        continue
    word, ipa, sampa, nix = line.split(',')
    if word.lower() in tts_lex:
        in_tts_lex.append(word + '\t' + ipa + '\t' + sampa)
    else:
        not_in_tts_lex.append(word + '\t' + ipa + '\t' + sampa)

    if '#' in sampa:
        print(line.strip())


with open('items_in_tts_lex.txt', 'w') as f:
    for item in in_tts_lex:
        f.write(item + '\n')

with open('items_NOT_in_tts_lex.txt', 'w') as f:
    for item in not_in_tts_lex:
        f.write(item + '\n')

