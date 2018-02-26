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


def is_compound(word):
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


def syllabify_on_subwords(entry, complist):
    """
    If entry is a compound, start syllabification on modifier-head
    :param entry:
    :return:
    """

    if len(entry.word) <= MIN_COMP_LEN:
        return

    word_to_divide = entry.word

    mod, head = is_compound(word_to_divide)
    if len(mod) > 0 and len(head) > 0:
        #print(mod + ' - ' + head)
        return

    elif len(head) > 0:
        #print(head + ' is a valid headword in: ' + word_to_divide)
        return

    elif len(word_to_divide) > 10:
        complist.append(word_to_divide)
        return


    return entry



def syllabify_on_nucleus(entry):
    """
    First round of syllabification. Divide the word such that each syllable
    starts with a vowel (except the first one, if the word starts with a consonant/consonants).
    """
    current_syllable = syllable.Syllable()
    for phone in entry.transcription_arr:
        if current_syllable.has_nucleus and phone in VOWELS:
            entry.syllables.append(current_syllable)
            current_syllable = syllable.Syllable()

        if phone in VOWELS:
            current_syllable.has_nucleus = True

        current_syllable.append(phone)
    # append last syllable
    entry.syllables.append(current_syllable)


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
    """

    for ind, syll in enumerate(entry.syllables):
        if ind == 0:
            continue
        prev_syll = entry.syllables[ind - 1]
        # syllable after the first syllable starts with a vowel - look for consonant onset in previous syllable
        # and move the consonant / consonant cluster from the previous to the current syllable
        if ind > 0 and syll.content[0] in VOWELS:
            if prev_syll.cons_cluster:
                # copy cons_cluster to next syllable
                syll.append_before(prev_syll.cons_cluster)
                prev_syll.remove_cluster()
                entry.update_syllables(ind, prev_syll, syll)
            elif prev_syll.last_phones() not in VOWELS:
                # handle 'jE' (=é) as one vowel
                if prev_syll.endswith('j') and syll.startswith('E'):
                    phone = prev_syll.last_phones(2)
                    syll.append_before(phone)
                    prev_syll.content = prev_syll.content[:-(len(phone)+1)]
                else:
                    phone = prev_syll.last_phones()
                    syll.append_before(phone)
                    prev_syll.content = prev_syll.content[:-(len(phone)+1)]
                entry.update_syllables(ind, prev_syll, syll)


def syllabify(entry, complist):

    syllabify_on_subwords(entry, complist)
    syllabify_on_nucleus(entry)
    identify_clusters(entry)
    syllabify_final(entry)

    return entry


def syllabify_dict(pron_dict):
    complist = []
    syllabified = []
    for entry in pron_dict:
        syllabify(entry, complist)
        syllabified.append(entry)

    complist.sort(key = lambda x: x[::-1])
    for comp in complist:
        print(comp)

    return syllabified



