#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dict_database import comp_dict_db
from dict_database import pron_dict_db


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


def contains_vowel(word):
    for c in word:
        if c in VOWELS:
            return True

    return False

def lookup_compound_components(word):
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

    if len(mod) == 0 and len(longest_valid_head) > 0:
        # assume we have a valid modifier anyway
        mod = word[:word.index(longest_valid_head)]
        # but only as long as it contains a vowel!
        if not contains_vowel(mod):
            mod = ''

    return mod, longest_valid_head


def extract_compound_components(comp_tree):
    """
    As long as compound components can be extracted, extract compound components and their transcripts recursively.

    :param comp_tree: a tree containing one root element. If compound components are found, they are added
    as children of the root.
    :return:
    """
    mod, head = lookup_compound_components(comp_tree.elem)
    if len(mod) > 0 and len(head) > 0:
        left_elem = mod
        left_tree = CompoundTree(left_elem)
        comp_tree.left = left_tree
        right_elem = head
        right_tree = CompoundTree(right_elem)
        comp_tree.right = right_tree
        extract_compound_components(left_tree)
        extract_compound_components(right_tree)


def build_compound_tree(word):
    """
    :param entry: a PronDictEntry
    :return: a binary tree based on compound division
    """

    comp_tree = CompoundTree(word)
    extract_compound_components(comp_tree)
    return comp_tree