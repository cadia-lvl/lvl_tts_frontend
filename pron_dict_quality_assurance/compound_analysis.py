#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import grapheme_phoneme_mapping
from dict_database import comp_dict_db
from dict_database import pron_dict_db
from pron_dict import entry
from grapheme_phoneme_mapping import G2P_align


VOWELS = ['a', 'á', 'e', 'é', 'i', 'í', 'o', 'ó', 'u', 'ú', 'y', 'ý', 'ö']
MODIFIER_MAP = comp_dict_db.get_modifier_map()
HEAD_MAP = comp_dict_db.get_head_map()
TRANSCR_MAP = pron_dict_db.get_transcriptions_map()
MIN_COMP_LEN = 4
MIN_INDEX = 2       # the position from which to start searching for a head word


class CompoundTree:
    def __init__(self, word):
        self.elem = word
        self.left = None
        self.right = None

    def preorder(self, elem_arr):
        if not self.left:
            #print(self.elem)
            elem_arr.append(self.elem)
        if self.left:
            self.left.preorder(elem_arr)
        if self.right:
            self.right.preorder(elem_arr)


def get_elem_transcriptions(elem_list, p_entry, g2p_map):
    elem_transcr_map = {}
    aligned = grapheme_phoneme_mapping.align_g2p(p_entry.word, p_entry.transcript, g2p_map)
    tuple_ind = 0
    elem_ind = 0
    for elem in elem_list:
        transcr = []
        for tuple in aligned[tuple_ind:]:
            grapheme = tuple[0]
            if elem[elem_ind: elem_ind + len(grapheme)] == grapheme:
                transcr.append(tuple[1])
                tuple_ind += 1
                elem_ind += len(grapheme)
            else:
                break

        elem_transcr_map[elem] = ' '.join(transcr)

    return elem_transcr_map


def contains_vowel(word):
    for c in word:
        if c in VOWELS:
            return True

    return False

def lookup_compound_components(word, p_dict={}):
    """
    Divides the word based on if its components are found in the compound database. The rule of thumb is that
    the longest possible head word shows the correct division, but if a modifier is found for a shorter
    head word, this one is chosen. If no modifier is found but a valid head word, the longest valid head word is
    returned, with the assumption that the modifier will also be valid, even if it is not in the dictionary.

    :param word:
    :return: extracted modifier and head if found, returns empty strings if no components are found
    """
    if len(word) <= MIN_COMP_LEN:
        return '', ''

    if word == 'félag' or word == 'félaga' or word == 'félags' or word == 'félagsins' or word == 'félögum':
        return '', ''

    n = MIN_INDEX
    longest_valid_head = ''
    mod = ''
    while n < len(word) - 2:
        head = word[n:]
        if head in HEAD_MAP:
            if word[:n] in MODIFIER_MAP:
                return word[:n], head
            elif longest_valid_head == '':
                longest_valid_head = head
        n += 1

    # if commented out: only components from database will make it into the results
    """
    if len(mod) == 0 and len(longest_valid_head) > 0:
        # assume we have a valid modifier anyway
        mod = word[:word.index(longest_valid_head)]
        if mod in p_dict:
            mod = 'frob_only_' + mod
        # but only as long as it contains a vowel!
        elif not contains_vowel(mod) or mod.startswith('guessed') or mod.startswith('frob_'):
            mod = ''
        elif not mod.startswith('guessed') and not mod.startswith('frob_'):
            mod = 'guessed_' + mod
    """
    return mod, longest_valid_head



def extract_compound_components(comp_tree, p_dict):
    """
    As long as compound components can be extracted, extract compound components and their transcripts recursively.

    :param comp_tree: a tree containing one root element. If compound components are found, they are added
    as children of the root.
    :return:
    """
    mod, head = lookup_compound_components(comp_tree.elem, p_dict)
    if len(mod) > 0 and len(head) > 0:
        left_elem = mod
        left_tree = CompoundTree(left_elem)
        comp_tree.left = left_tree
        right_elem = head
        right_tree = CompoundTree(right_elem)
        comp_tree.right = right_tree
        extract_compound_components(left_tree, p_dict)
        extract_compound_components(right_tree, p_dict)


def build_compound_tree(word, p_dict={}):
    """
    :param entry: a PronDictEntry
    :return: a binary tree based on compound division
    """

    comp_tree = CompoundTree(word)
    extract_compound_components(comp_tree, p_dict)
    return comp_tree


def get_compounds(p_dict, g2p):
    for word in p_dict.keys():
        tree = build_compound_tree(word, p_dict)
        comp_elems = []
        tree.preorder(comp_elems)
        if len(comp_elems) > 1:
            # align transcript using grapheme_phoneme_mapping of word and extract the transcript for each element
            elem_dict = get_elem_transcriptions(comp_elems, p_dict[word], g2p.g2p_map)
            p_dict[word].compound_elements = comp_elems
            for elem in comp_elems:
                if elem in p_dict:
                    p_dict[elem].frequency += 1
                    p_dict[elem].transcript_variants.add(elem_dict[elem])

    return p_dict


def main():

    frob_in = open(sys.argv[1]).readlines()

    pron_dict = {}

    for line in frob_in:
        word, transcr = line.strip().split('\t')
        dict_entry = entry.PronDictEntry(word, transcr)
        dict_entry.frequency = 1
        pron_dict[word.lower()] = dict_entry

    g2p = G2P_align(frob_in, 1000)
    g2p.extend_mapping(frob_in)

    pron_dict = get_compounds(pron_dict, g2p)

    with open('pron_dict_compounds_variants.txt', 'w') as f:
        for word in sorted(pron_dict, key=lambda x: pron_dict[x].frequency, reverse=True):
            elem = pron_dict[word]
            if elem.frequency > 1: #len(elem.compound_elements) > 1: #
                f.write(word + '\t' + elem.transcript + '\t' + str(elem.compound_elements) +
                        '\t' + str(elem.transcript_variants) + str(elem.frequency))
                f.write('\n')
                """
                for e in elem.compound_elements:
                    if e.startswith('frob_only'):
                        
                        break
                """


if __name__ == '__main__':
    main()

