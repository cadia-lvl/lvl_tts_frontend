#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
The pron_dict module processes an ASR pronunciation dictionary, containing entries of the form 'word     transcription',
computes the necessary additional information for TTS (part-of-speech, syllabification and stress marks) and
outputs the results in the Festvox format.

Example:
    Input entry:

    adolfsdóttir     a: t O l f s t ou h d I r

    Output entry:

    ("adolfsdóttir" n (((a:) 1) ((t O l f s) 3) ((t ou h) 1) ((d I r) 3)))


"""
__license__ = 'Apache 2.0 (see: LICENSE)'

import argparse
import gpos

from entry import PronDictEntry


def init_pron_dict(dict_file):
    pron_dict = []

    for line in dict_file:
        word, transcr = line.split('\t')
        pron_dict.append(PronDictEntry(word, transcr))

    return pron_dict


def parse_args():
    parser = argparse.ArgumentParser(description='pronunciation dictionary for TTS', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('i', type=argparse.FileType('r'), help='ASR pronunciation dictionary')
   # parser.add_argument('o', type=argparse.FileType('w'), default='', help='Output: TTS pronunciation dictionary')

    return parser.parse_args()


def main():

    args = parse_args()
    pron_dict = init_pron_dict(args.i)
    gpos.perform_gpos_for_entry_list(pron_dict)


if __name__ == '__main__':
    main()
