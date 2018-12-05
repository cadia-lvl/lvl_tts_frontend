#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test the quality of automatic syllabification.


"""

from pron_dict import entry
from pron_dict import syllabification
from pron_dict import tree_builder

import difflib


def get_syllable_arr(syllables):
    syllable_arr = []
    for syll in syllables:
        syllable_arr.append(syll.content)

    return syllable_arr


def syllabify(pron_dict_entry):
    comp_tree = tree_builder.build_compound_tree(pron_dict_entry)
    syllables = []
    syllabification.syllabify_tree(comp_tree, syllables)
    res_syllables = get_syllable_arr(syllables)
    return res_syllables


test_file = open('data/syllab_dev_87.txt')
test_data = test_file.readlines()

errors = []
for line in test_data:
    word, transcr = line.split('\t')
    clean_transcr = transcr.replace(' |', '').strip()
    pron_dict_entry = entry.PronDictEntry(word, clean_transcr)
    syllables = syllabify(pron_dict_entry)
    syllab_string = '| '.join(syllables)

    #diff = difflib.Differ()
    #print(list(diff.compare(transcr.strip(), syllab_string)))

    if syllab_string.strip() != transcr.strip():
        errors.append(word + '\t' + transcr.strip() + '\t' + syllab_string)

print('Errors: ' + str(len(errors)))
print('Error rate: ' + str((len(errors)/len(test_data)) * 100.0) + '%')

with open('syllab_test_results_87.txt', 'w') as f:
    f.write('Errors: ' + str(len(errors)) + '\n')
    f.write('Error rate: ' + str((len(errors) / len(test_data)) * 100.0) + '%\n')
    for entry in errors:
        f.write(entry + '\n')