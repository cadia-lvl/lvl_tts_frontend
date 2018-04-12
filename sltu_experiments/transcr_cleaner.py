#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Clean ossian formatted transcripts.

Remove syllable symbol, and, if wanted, stress marks

"""

import sys
import re

def clean_transcript(transcr, rm_stress):
    clean_transcr = transcr.replace('|', '')
    clean_transcr = re.sub(r'\s+', ' ', clean_transcr)
    if rm_stress:
        stress_removed = []
        for phone in clean_transcr.split():
            if re.match('.+[01]', phone) and not re.match('.+_0', phone):
                phone = phone.replace('0', '')
                phone = phone.replace('1', '')
            stress_removed.append(phone)

        clean_transcr = ' '.join(stress_removed)

    return clean_transcr


remove_stress = False

in_file = sys.argv[1]
clean_file = sys.argv[2]

if len(sys.argv) > 3 and sys.argv[3] == '1':
    remove_stress = True

clean = []

for line in open(in_file).readlines():
    entry, transcr = line.split('\t')
    clean_tr = clean_transcript(transcr, remove_stress)
    clean.append(entry + '\t' + clean_tr)

with open(clean_file, 'w') as f:
    for entry in clean:
        f.write(entry)
        f.write('\n')
