#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test the quality of automatic compound/derivation splitting

"""

from pron_dict import tree_builder
from pron_dict import entry


def traverse_tree(entry_tree, comp_elems):
    """
    Recursively call traverse_tree on each element of entry_tree.
    Append the transcripts of the leaf nodes to the argument array.
    :param entry_tree: a binary tree of a compound structure, the tree might not have any leaves,
    i.e. is not necessarily a compound
    :param syllables: an array to add up the leaf syllables of the tree
    :return:
    """
    if not entry_tree.left:
        comp_elems.append(entry_tree.elem.transcript)
    if entry_tree.left:
        traverse_tree(entry_tree.left, comp_elems)
    if entry_tree.right:
        traverse_tree(entry_tree.right, comp_elems)


test_file = open('data/compounds_dev_87.txt')
test_data = test_file.readlines()

errors = []

for line in test_data:
    word, transcr = line.split('\t')
    clean_transcr = transcr.replace(' -', '').strip()
    comp_tree = tree_builder.build_compound_tree(
            entry.PronDictEntry(word, clean_transcr))

    result = []
    traverse_tree(comp_tree, result)
    splitted = ' - '.join(result).strip()
    if splitted != transcr.strip():
        errors.append(word + '\t' + transcr.strip() + '\t' + splitted)


print('Errors: ' + str(len(errors)))
print('Error rate: ' + str((len(errors) / len(test_data)) * 100.0) + '%')

with open('compounds_test_results_87.txt', 'w') as f:
    f.write('Errors: ' + str(len(errors)) + '\n')
    f.write('Error rate: ' + str((len(errors) / len(test_data)) * 100.0) + '%\n')
    for entry in errors:
        f.write(entry + '\n')
