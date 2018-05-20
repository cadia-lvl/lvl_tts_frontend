#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Count the different errors found during align process (align_phonemes (IPA) or align_sampa.py).

The most common errors from sampa were identified by grep, the rest labeled manually.

We assume only one error per transcript, there could of course be more, but that is not highly relevant at this step.

Input format:

"Invalid symbol found in "transcription""   error-symbol

"""

import sys

in_file = sys.argv[1]

error_dict = {}

for line in open(in_file).readlines():
    #print(line)
    if len(line.split('\t')) != 2:
        print(line.strip())
        continue
    explanation, symbol = line.strip().split('\t')

    error_dict[symbol] = error_dict[symbol] + 1 if symbol in error_dict else 1

for key in sorted(error_dict.keys()):
    print(key + '\t' + str(error_dict[key]))

