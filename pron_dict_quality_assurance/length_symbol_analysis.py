#!/usr/bin/env python3

# Where are length symbols used in the pron dictionary?
# Collect all transcripts with length symbols that are not only at the first vowel

import sys

VOWELS = ['a', 'a:', 'ai', 'au', 'au:', 'ei', 'ei:', 'i', 'i:', 'ou', 'ou:', 'u', 'u:', '9', '9:' ,'9Y', '9Y:',
          'O', 'Oi', 'O:', 'E', 'E:', 'I', 'I:', 'Y', 'Y:' 'Yi']

LENGTH_SYMBOL = ':'

pron_dict = open(sys.argv[1]).readlines()

length_symbol_transcripts = []

# analyse:
for line in pron_dict:
    word, transcr = line.strip().split('\t')
    t_arr = transcr.split()
    vowel_seen = False
    for phon in t_arr:
        if phon in VOWELS:
            if vowel_seen and LENGTH_SYMBOL in phon:
                length_symbol_transcripts.append(line.strip())

                break
            else:
                vowel_seen = True

#for line in length_symbol_transcripts:
#    print(line)


# clean:

results = []
for line in pron_dict:
    word, transcr = line.strip().split('\t')
    t_arr = transcr.split()
    vowel_seen = False
    for ind, phon in enumerate(t_arr):
        if phon in VOWELS:
            if vowel_seen and LENGTH_SYMBOL in phon:
                phon = phon.replace(':', '')
                t_arr[ind] = phon
            else:
                vowel_seen = True

    new_transcr = ' '.join(t_arr)

    results.append(word + '\t' + new_transcr)

for line in results:
    print(line)
