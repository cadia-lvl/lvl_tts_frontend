#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test the quality of automatic stress labeling.


"""

import re
import syllabification
import stress
import tree_builder

from entry import PronDictEntry


def remove_stress(transcription):
    stress_removed = []
    for phone in transcription.split():
        if re.match('.+[01]', phone) and not re.match('.+_0', phone):
            phone = phone.replace('0', '')
            phone = phone.replace('1', '')
        stress_removed.append(phone)

    return ' '.join(stress_removed)


def init_pron_dict(dict_file):
    pron_dict = []
    for line in dict_file:
        word, transcr = line.split('\t')
        clean_transcr = remove_stress(transcr)
        entry = PronDictEntry(word, clean_transcr)
        pron_dict.append(entry)
    return pron_dict


def create_tree_list(pron_dict):

    tree_list = []
    for entry in pron_dict:
        t = tree_builder.build_compound_tree(entry)
        tree_list.append(t)
    return tree_list


def main():

    test_file = open('data/g2p/g2p_dev_stress_87.txt')
    test_data = test_file.readlines()
    pron_dict = init_pron_dict(test_data)

    tree_dict = create_tree_list(pron_dict)

    syllabified = syllabification.syllabify_tree_dict(tree_dict)
    syllab_with_stress = stress.set_stress(syllabified)

    errors = []

    for i in range(len(syllab_with_stress)):
        stress_test = syllab_with_stress[i].simple_stress_format()
        word, transcr = test_data[i].split('\t')
        if word != syllab_with_stress[i].word:
            print('WORDS DO NOT MATCH! ' + word + ' - ' + syllab_with_stress[i].word)

        elif transcr.strip() != stress_test:
            errors.append(word + '\t' + transcr.strip() + '\t' + stress_test)

    print('Errors: ' + str(len(errors)))
    print('Error rate: ' + str((len(errors) / len(test_data)) * 100.0) + '%')

    with open('stress_test_results_87.txt', 'w') as f:
        f.write('Errors: ' + str(len(errors)) + '\n')
        f.write('Error rate: ' + str((len(errors) / len(test_data)) * 100.0) + '%\n')
        for entry in errors:
            f.write(entry + '\n')



if __name__ == '__main__':
    main()
