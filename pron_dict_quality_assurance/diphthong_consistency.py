#!/usr/bin/env python3

"""
Ensure that all diphthongs are transcribed in the same way:

    'ei/ey'     /ei(ː)/
    'au'        /œy(ː)/
    'æ'         /ai(ː)/
    'ó'         /ou(ː)/
    'á'         /au(ː)/

    'ugi'       /ʏi j ɪ/
    'ogi'       /ɔi j ɪ/

    'agi'       /ai j ɪ/
    'an[gk]'    /au/
    'eg[ij]'    /ei j (ɪ)/
    'en[gk]'    /ei/
    'un[gk]'    /u/
    'ögi'       /œy j ɪ/
    'ön[gk]'    /œy/
    '[iy]n[gk]' /i/

1) collect statistics on how the transcriptions of the above are in original (IPA-valid) frob
2) write out correct and non-correct entries

We will not correct the entries, but rather remove them from the dictionary and later transcribe them via g2p

Input: aligned frob file of the format:

a	aː
abbast	a p a s t
Adam	aː t a m
Adams	aː t a m s
...


"""

import sys
import re

# the transcription of the following words should not be treated as errors
exception_list = ['andagift',
                  'Hrafnagili',
                  'Kjærnested',
                  'liðagigt',
                  'liðagigtar',
                  'magister',
                  'notagildi',
                  'notagildis',
                  'Alzheimer',
                  'stöðugildi',
                  'stöðugildum']

regex_dict = { re.compile('æ|agi'): 'ai',
                    re.compile('ó|on[gk]'): 'ou',
                    re.compile('ei|ey|en[gk]|eg[ij]]'): 'ei',
                    re.compile('au|ön[gk]|ögi'): 'œy',
                    re.compile('á|an[gk]'): 'au',
                    re.compile('[^a]ugi'): 'ʏi j ɪ',
                    re.compile('ogi'): 'ɔi j ɪ',
            }


def main():
    frob_file = sys.argv[1]
    correct = []
    error = []
    for line in open(frob_file).readlines():
        word, transcr = line.strip().split('\t')
        if word in exception_list:
            continue
        for pattern in regex_dict.keys():
            if pattern.search(word):
                if re.search(regex_dict[pattern], transcr):
                    correct.append(line.strip())
                else:
                    error.append(line.strip())

    #print("ERRORS: " + str(len(error)))
    for line in error:
        print(line)

    #print("==============CORRECT=============== " + str(len(correct)))
    #for line in correct:
    #    print("correct " + line)


if __name__ == '__main__':
    main()