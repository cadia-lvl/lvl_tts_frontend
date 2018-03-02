#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import compounds
import tree
import entry


MODIFIER_MAP = compounds.get_modifier_map()
HEAD_MAP = compounds.get_head_map()
TRANSCR_MAP = compounds.get_transcriptions_map()
MIN_COMP_LEN = 4
MIN_INDEX = 2       # the position from which to start searching for a head word


def compare_transcripts(comp_transcript, head_transcript):
    """
    If a transcript differs only in a length mark or in voiced/voiceless or having post aspriation or not,
    it should be recognized as the same transcript (since we have already matched the corresponding word strings)
    """

    head_ind = len(head_transcript) - 1
    comp_ind = len(comp_transcript) - 1

    while head_ind >= 0:
        if head_transcript[head_ind] == comp_transcript[comp_ind]:
            head_ind -= 2
            comp_ind -= 2
        elif head_transcript[head_ind] == ':':
            head_ind -= 1
        elif comp_transcript[comp_ind] == ':':
            comp_ind -= 1
        elif head_transcript[head_ind] == '0' or head_transcript[head_ind] == 'h':
            head_ind -= 2
        elif comp_transcript[comp_ind] == '0' or comp_transcript[comp_ind] == 'h':
            comp_ind -= 2
        elif head_ind == 0:
            return comp_ind
        else:
            return -1

    return comp_ind + 2 # make up for the last iteration where head_ind went below 0



def extract_transcription(entry, comp_mod, comp_head):
    """
    - find index of comp_head
    - find mapping phone
    - search for phone index in phone string (note that phones are space separated!
    - create two syllables: one with fixed end (mod) and one with fixed start (head)
    :param entry:
    :param comp_head:
    :return:
    """

    head_transcr = TRANSCR_MAP[comp_head]
    head_syllable_index = entry.transcript.rfind(head_transcr)
    # words with long vowels might not be transcribed as containing a long vowel in the compound.
    # l E: G Y vs. s k r 9Y: t l E G Y
    if head_syllable_index <= 0:
       head_syllable_index = compare_transcripts(entry.transcript, head_transcr)
    if head_syllable_index <= 0:
        print("did not find transcription of " + comp_head + "!")
        print("transcription in db: " + head_transcr + ", compound transcr: " + entry.transcript)
        return '', ''

    else:

        modifier_transcr = entry.transcript[0:head_syllable_index]
        head_transcr = entry.transcript[head_syllable_index:]
        return modifier_transcr, head_transcr


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
        mod = word[:word.index(longest_valid_head)]

    return mod, longest_valid_head


def extract_compound_components(comp_tree):

    mod, head = lookup_compound_components(comp_tree.elem.word)
    if len(mod) > 0 and len(head) > 0:
        mod_transcr, head_transcr = extract_transcription(comp_tree.elem, mod, head)
        if len(mod_transcr) > 0 and len(head_transcr) > 0:
            left_elem = entry.PronDictEntry(mod, mod_transcr)
            left_tree = tree.CompoundTree(left_elem)
            comp_tree.left = left_tree
            right_elem = entry.PronDictEntry(head, head_transcr)
            right_tree = tree.CompoundTree(right_elem)
            comp_tree.right = right_tree
            extract_compound_components(left_tree)
            extract_compound_components(right_tree)


def build_compound_tree(entry):
    """
    :param entry:
    :return: a binary tree based on compound division
    """

    comp_tree = tree.CompoundTree(entry)
    extract_compound_components(comp_tree)
    return comp_tree

