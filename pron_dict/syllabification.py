#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

Perform syllabification on words transcribed with X-SAMPA.
Syllable rules for Icelandic as described in:
    - Anton Karl Ingason (2006): Íslensk atkvæði - vélræn nálgun. (http://www.linguist.is/skjol/atkvadi.pdf)
    - Kristján Árnason (2005): Hljóð. Ritröðin Íslensk tunga.

The basic assumption is that Icelandic syllable structure follows the onset-rhyme model. From this follows that,
whenever possible, a syllable has a 'need' for an onset consonant. This contradicts in some cases with rules for
'between-the-lines' word division rules saying that a word should be divided between lines
such that the next line starts with a vowel: 'hes.tur' vs. 'hest.ur'.

The following consonant combinations always build an onset together (i.e. the second one should not be the onset
for the next syllable):

    s, p, t, k + v, j, r    (sv, sj, sr, pv, pj, pr, etc.)
    br
    fr

# input: transcribed and aligned word, example: p r I c Y k v E r v I (bryggjuhverfi)
# output: syllabified word: prI-cY-kvEr-vI (bry-ggju-hver-fi)

# algorithm:
# 1) symbols upto the second vowel build the first syllable: 'prIc'
# 2) the remaining string is divided into syllables each starting with a vowel: 'prIc-Ykv-Erv-I'
# 3) identify cons cluster: 'prIc-Y(kv)-Erv-I'
# 4) move consonants to onset: 'prI-cY-kvEr-vI'

"""

import syllable


# each syllable has a vowel as a nucleus. 'e' and 'o' aren't actually in the inventory, but we need
# to be able to identify 'ei' and 'ou' from the first character only
VOWELS = ['a', 'a:', 'O', 'O:', 'u', 'u:', '9', '9:', 'Y', 'Y:', 'E', 'E:', 'I', 'I:', 'i', 'i:',
          'ai', 'ai:', 'au', 'au:', 'ou', 'ou:', '9Y', '9Y:', 'Oi', 'Yi', 'ei', 'ei:', 'e', 'o']

# these consonant clusters should not be divided between two syllables
# the general rule is: p, t, k, s, b, d, g, f + v, j, r. But not all of these combinations are
# valid ('sr', 'pv', 'fv')
CONS_CLUSTERS = ['s v', 's j', 'p j', 'p r', 't v', 't j', 't r', 'k v', 'k j', 'k r',
                 'p_h j', 'p_h r', 't_h v', 't_h j', 't_h r', 'k_h v', 'k_h j', 'k_h r', 'f r', 'f j']



def divide_syllable(syllable):
    transcr_arr = syllable.content.split()
    syllables = syllabify_on_nucleus(transcr_arr)
    if syllable.fixed_start:
        syllables[0].fixed_start = True
    if syllable.fixed_end:
        syllables[len(syllables) - 1].fixed_end = True

    return syllables


def syllabify_compound(entry):

    new_syllables = []
    for syll in entry.syllables:
        new_syllables = new_syllables + divide_syllable(syll)

    return new_syllables


def syllabify_on_nucleus(transcription_arr):
    """
    First round of syllabification. Divide the word such that each syllable
    starts with a vowel (except the first one, if the word starts with a consonant/consonants).
    """
    syllables = []
    current_syllable = syllable.Syllable()
    for phone in transcription_arr:
        if current_syllable.has_nucleus and phone in VOWELS:
            syllables.append(current_syllable)
            current_syllable = syllable.Syllable()

        if phone in VOWELS:
            current_syllable.has_nucleus = True

        current_syllable.append(phone)
    # append last syllable
    syllables.append(current_syllable)
    return syllables


def identify_clusters(entry):
    for syll in entry.syllables:
        for clust in CONS_CLUSTERS:
            if syll.content.strip().endswith(clust):
                syll.cons_cluster = clust


def syllabify_final(entry):
    """
    Iterate once more over the syllable structure and move consonants from rhyme to onset
    where appropriate, i.e. where one syllable ends with a consonant and the
    next one starts with a vowel. If a syllable ends with a consonant cluster, the whole
    cluster is moved to the next syllable, otherwise only the last consonant.
    However, if a syllable has a fixed boundary (as a result of decompounding), end or start,
    the boundary can not be changed.
    """

    for ind, syll in enumerate(entry.syllables):
        if ind == 0:
            continue
        prev_syll = entry.syllables[ind - 1]
        # syllable after the first syllable starts with a vowel - look for consonant onset in previous syllable
        # and move the consonant / consonant cluster from the previous to the current syllable
        if ind > 0 and syll.content[0] in VOWELS:
            if prev_syll.cons_cluster and not prev_syll.fixed_end:
                # copy cons_cluster to next syllable
                syll.append_before(prev_syll.cons_cluster)
                prev_syll.remove_cluster()
                entry.update_syllables(ind, prev_syll, syll)
            elif prev_syll.last_phones() not in VOWELS and not prev_syll.fixed_end:
                # handle 'jE' (=é) as one vowel
                if prev_syll.endswith('j') and syll.startswith('E'):
                    phone = prev_syll.last_phones(1)
                    syll.append_before(phone)
                    prev_syll.content = prev_syll.content[:-(len(phone)+1)]
                else:
                    phone = prev_syll.last_phones()
                    syll.append_before(phone)
                    prev_syll.content = prev_syll.content[:-(len(phone)+1)]
                entry.update_syllables(ind, prev_syll, syll)


def syllabify_entry(entry):

    entry.syllables = syllabify_on_nucleus(entry.transcription_arr)
    identify_clusters(entry)
    syllabify_final(entry)


def syllabify_tree(entry_tree, syllables):
    if not entry_tree.left:
        syllabify_entry(entry_tree.elem)
        syllables += entry_tree.elem.syllables
    if entry_tree.left:
        syllabify_tree(entry_tree.left, syllables)
    if entry_tree.right:
        syllabify_tree(entry_tree.right, syllables)


def syllabify_tree_dict(tree_dict):

    syllabified = []
    for entry in tree_dict:
        syllabify_tree(entry)

        syllabified.append(entry)

    return syllabified


def syllabify_dict(pron_dict):

    syllabified = []
    for entry in pron_dict:
        syllabify_entry(entry)
        syllabified.append(entry)

    return syllabified



