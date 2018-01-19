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

def parse_args():
    parser = argparse.ArgumentParser(description='description of project/program', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('i', type=argparse.FileType('r'), help='Input data')
    parser.add_argument('o', type=argparse.FileType('w'), help='Output file')
    parser.add_argument('--some_int_arg', default=10)
    parser.add_argument('--some_string_arg', default='ent')

    return parser.parse_args()


def main():

    args = parse_args()


if __name__ == '__main__':
    main()
