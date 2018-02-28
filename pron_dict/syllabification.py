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
import compounds
import letters


# each syllable has a vowel as a nucleus. 'e' and 'o' aren't actually in the inventory, but we need
# to be able to identify 'ei' and 'ou' from the first character only
VOWELS = ['a', 'a:', 'O', 'O:', 'u', 'u:', '9', '9:', 'Y', 'Y:', 'E', 'E:', 'I', 'I:', 'i', 'i:',
          'ai', 'ai:', 'au', 'au:', 'ou', 'ou:', '9Y', '9Y:', 'Oi', 'Yi', 'ei', 'ei:', 'e', 'o']

# these consonant clusters should not be divided between two syllables
# the general rule is: p, t, k, s, b, d, g, f + v, j, r. But not all of these combinations are
# valid ('sr', 'pv', 'fv')
CONS_CLUSTERS = ['s v', 's j', 'p j', 'p r', 't v', 't j', 't r', 'k v', 'k j', 'k r',
                 'p_h j', 'p_h r', 't_h v', 't_h j', 't_h r', 'k_h v', 'k_h j', 'k_h r', 'f r', 'f j']


MODIFIER_MAP = compounds.get_modifier_map()
HEAD_MAP = compounds.get_head_map()
MIN_COMP_LEN = 4
MIN_INDEX = 2


def extract_compound_components(word):
    """
    TODO: this could search more exhaustingly for a valid modifier and head. Now only the longest possible head
    is extracted, regardless if a valid modifier is found or not. Possibly a shorter head would allow for
    a valid modifier.

    :param word:
    :return: extracted modifier and head if found, otherwise an empty string for each not found component
    """
    n = MIN_INDEX

    while n < len(word) - 2:
        head = word[n:]
        if head in HEAD_MAP:
            if word[:n] in MODIFIER_MAP:
                return word[:n], head
            else:
                return '', head
        n += 1

    return '', ''


def fix_compound_boundary(entry, comp_head):
    """
    - find index of comp_head
    - find mapping phone
    - search for phone index in phone string (note that phones are space separated!
    - create two syllables: one with fixed end (mod) and one with fixed start (head)
    :param entry:
    :param comp_head:
    :return:
    """

    transcr_index = len(entry.transcription_arr) - 1
    head_transcr = ''
    for c in comp_head[::-1]:
        if entry.transcription_arr[transcr_index] in letters.LETTER2PHONE_MAP[c]:
            head_transcr = entry.transcription_arr[transcr_index] + ' ' + head_transcr
            transcr_index -= 1
        else:
            break

    if len(head_transcr) == 0:
        return
    else:
        modifier_syll = syllable.Syllable()
        modifier_syll.content = ' '.join(entry.transcription_arr[0:transcr_index+1])
        modifier_syll.fixed_end = True
        head_syll = syllable.Syllable()
        head_syll.content = head_transcr
        head_syll.fixed_start = True
        entry.syllables.append(modifier_syll)
        entry.syllables.append(head_syll)
        entry.is_compound = True


def syllabify_on_subwords(entry):
    """
    If entry is a compound, start syllabification on modifier-head
    :param entry:
    :return:
    """

    if len(entry.word) <= MIN_COMP_LEN:
        return entry

    word_to_divide = entry.word

    mod, head = extract_compound_components(word_to_divide)
    # TODO: do both parts need to be valid?
    if len(mod) > 0 and len(head) > 0:
        fix_compound_boundary(entry, head)

    elif len(head) > 0:
        fix_compound_boundary(entry, head)

    return entry


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


def syllabify(entry):

    syllabify_on_subwords(entry)
    if entry.is_compound:
        entry.syllables = syllabify_compound(entry)
    else:
        entry.syllables = syllabify_on_nucleus(entry.transcription_arr)
    identify_clusters(entry)
    syllabify_final(entry)

    return entry


def syllabify_dict(pron_dict):

    syllabified = []
    for entry in pron_dict:
        syllabify(entry)
        syllabified.append(entry)

    return syllabified



