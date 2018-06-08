#!/usr/bin/env python3

# Where are length symbols used in the pron dictionary?
# Collect all transcripts with length symbols that are not only at the first vowel

import sys

XSAMPA_VOWELS = ['a', 'a:', 'ai', 'au', 'au:', 'ei', 'ei:', 'i', 'i:', 'ou', 'ou:', 'u', 'u:', '9', '9:' ,'9Y', '9Y:',
          'O', 'Oi', 'O:', 'E', 'E:', 'I', 'I:', 'Y', 'Y:' 'Yi']

IPA_VOWELS = ['a', 'aː', 'ai', 'au', 'auː', 'ei', 'eiː', 'i', 'iː', 'ou', 'ouː', 'u', 'uː', 'œ', 'œː' ,'œy', 'œyː',
          'ɔ', 'ɔi', 'ɔː', 'ɛ', 'ɛː', 'ɪ', 'ɪː', 'ʏ', 'ʏː' 'ʏi']

XSAMPA_LENGTH_SYMBOL = ':'
IPA_LENGTH_SYMBOL = 'ː'


def remove_all_length_symbols(phon_arr, vowel_set, length_symbol):

    for ind, phon in enumerate(phon_arr):
        if phon in vowel_set and length_symbol in phon:
            phon = phon.replace(length_symbol, '')
            phon_arr[ind] = phon

    new_transcr = ' '.join(phon_arr)

    return new_transcr


def find_length_symbol_after_1st(pron_dict, vowel_set, length_symbol):
    length_symbol_transcripts = []
    for line in pron_dict:
        word, transcr = line.strip().split('\t')
        t_arr = transcr.split()
        vowel_seen = False
        for phon in t_arr:
            if phon in vowel_set:
                if vowel_seen and length_symbol in phon:
                    length_symbol_transcripts.append(line.strip())
                    break
                else:
                    vowel_seen = True

    return length_symbol_transcripts


def remove_late_length_symbols(phon_arr, vowel_set, length_symbol):
    vowel_seen = False
    for ind, phon in enumerate(phon_arr):
        if phon in vowel_set:
            if vowel_seen and length_symbol in phon:
                phon = phon.replace(length_symbol, '')
                phon_arr[ind] = phon
            else:
                vowel_seen = True

    new_transcr = ' '.join(phon_arr)
    return new_transcr


def main():

    pron_dict = open(sys.argv[1]).readlines()
    results = []
    for line in pron_dict:
        word, transcr = line.strip().split('\t')
        t_arr = transcr.split()

        results.append(remove_all_length_symbols(t_arr, IPA_VOWELS, IPA_LENGTH_SYMBOL))

    for line in results:
        print(line)


if __name__ == '__main__':
    main()