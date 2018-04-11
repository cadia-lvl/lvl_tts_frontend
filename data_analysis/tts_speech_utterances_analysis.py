#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Analyse a summary textfile from TTS speech recordings

Google is format (e.g. line_index_m/f.txt):

speaker_id_utt_id   email   some-id  utterance

Google ban format (e.g. bangla_line_index.tsv):

speaker_id_utt_id   utterance

Ivona format (e.g. ivona_demo2000.txt):

utterance


Collect:

1) Number of distinct speakers
2) Number of utterances per speaker
3) Number of unique utterances
4) Number of unique tokens (lowercased, punctuation stripped)
5) Word frequency list

"""

import sys
import re
from nltk.util import ngrams

in_file = open(sys.argv[1])
pron_dict_file = sys.argv[2]
out_dir = sys.argv[3]


speaker_dict = {}
utterance_dict = {}
token_dict = {}
bigram_dict = {}
quingram_dict = {}
non_normalized = []
oov = set()

sum_utt_len = 0
no_of_lines = 0

letters = '^[a-záéíóúýæöðþ, ]+$'
full_stops = '.+[.,:;?!]'

# pronunciation dictionary for oov-check
pron_dict = []
for line in open(pron_dict_file).readlines():
    arr = line.split('\t')
    pron_dict.append(arr[0])

# collect information from utterances file
for line in in_file.readlines():

    # google is format?
    if len(line.split('\t')) == 4:
        utt_id, email, sha, utt = line.split('\t')
        # speaker data is only available for google format
        speaker_id = utt_id[:8]
        speaker_dict[speaker_id] = speaker_dict[speaker_id] + 1 if speaker_id in speaker_dict else 1

    # google bangla format?
    elif len(line.split('\t')) == 2:
        utt_id, utt = line.split('\t')
        # speaker data
        speaker_id = utt_id[:9]
        speaker_dict[speaker_id] = speaker_dict[speaker_id] + 1 if speaker_id in speaker_dict else 1
    # ivona format
    else:
        utt = line.strip()

    # utterance data
    utterance_dict[utt] = utterance_dict[utt] + 1 if utt in utterance_dict else 1
    utt_lower = utt.lower().strip()

    if re.match(full_stops, utt_lower):
        utt_lower = utt_lower[:-1]
    if not re.match(letters, utt_lower):
        non_normalized.append(utt_lower)

    # token analysis
    tok_arr = utt_lower.split()
    for tok in tok_arr:
        if tok.endswith('*'):
            tok = tok[:-1]
        if tok.endswith('.') or tok.endswith(','):
            tok = tok[:-1]
        if tok not in pron_dict:
            oov.add(tok)
        token_dict[tok] = token_dict[tok] + 1 if tok in token_dict else 1

    sum_utt_len += len(tok_arr)
    no_of_lines += 1

    # n-gram analysis (character based)
    chrs = [c for c in utt_lower]
    bigrams = ngrams(chrs, 2)
    for bigram in bigrams:
        bigram_dict[bigram] = bigram_dict[bigram] + 1 if bigram in bigram_dict else 1

    quingrams = ngrams(chrs, 5)
    for quingram in quingrams:
        quingram_dict[bigram] = quingram_dict[bigram] + 1 if quingram in quingram_dict else 1


# print the results

avg_utt_len = sum_utt_len/float(no_of_lines)
print('avg utt len: ' + str(avg_utt_len))


def write_dict(filename, out_dict):
    out_tuples = [(v,k) for k,v in out_dict.items()]
    out_tuples.sort(reverse=True)

    out = open(filename, 'w')
    for v, k in out_tuples:
        out.write(str(k) + '\t' + str(v))
        out.write('\n')

    out.close()


def write_list(filename, list2write):
    out = open(filename, 'w')
    for it in list2write:
        out.write(it + '\n')

    out.close()


if len(speaker_dict) > 0:
    write_dict(out_dir + '/speaker_stats.txt', speaker_dict)

write_dict(out_dir + '/utterance_stats.txt', utterance_dict)
write_dict(out_dir + '/token_stats.txt', token_dict)
write_dict(out_dir + '/bigram_stats.txt', bigram_dict)
write_dict(out_dir + '/quingram_stats.txt', quingram_dict)

write_list(out_dir + '/oov.txt', oov)
write_list(out_dir + '/non_normalized.txt', non_normalized)
