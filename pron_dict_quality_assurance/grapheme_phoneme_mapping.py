#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

SHORT_VOWELS = ['a', 'E', 'I', 'i', 'O', 'Y', 'u', '9', 'ai', 'ei', 'Ou', '9Y']
LONG_VOWELS = ['a:', 'E:', 'I:', 'i:', 'O:', 'Y:', 'u:', '9:', 'ai:', 'ei:', 'Ou:', '9Y:']


class G2P_align:

    def __init__(self, prondict_list, min_occur=1000):
        self.g2p_map = {}
        self.one_on_one_map = self.init_map(prondict_list)
        self.init_g2p_map(self.one_on_one_map, min_occur)
        self.add_special_mappings()

    def init_map(self, p_list):
        one_on_one_map = {}
        for line in p_list:
            word, transcr = line.strip().split('\t')
            tuples = self.map_g2p_one_on_one(word, transcr)
            for t in tuples:
                if t in one_on_one_map:
                    one_on_one_map[t] = one_on_one_map[t] + 1
                else:
                    one_on_one_map[t] = 1
        return one_on_one_map

    def map_g2p_one_on_one(self, word, transcript):
        """
        Get basic g2p mapping, only create mappings for word-transcript pairs that are equally long.
        :param word:
        :param transcript:
        :return: a list of g2p tuples if mapped, an empty list otherwise
        """
        word_arr = list(word)
        tr_arr = transcript.split()

        tuples = []
        if len(word_arr) != len(tr_arr):
            return tuples
        for ind, c in enumerate(word_arr):
            tuples.append((c.lower(), tr_arr[ind]))

        return tuples

    def init_g2p_map(self, map_to_filter, min_occur):
        self.g2p_map = {}
        for t in map_to_filter.keys():
            if map_to_filter[t] > min_occur:
                if t[0] in self.g2p_map:
                    self.g2p_map[t[0]].append(t[1])
                else:
                    self.g2p_map[t[0]] = [t[1]]

    def extend_mapping(self, prondict_list, min_occur=100):
        extended_g2p_map = {}
        for line in prondict_list:
            word, transcr = line.strip().split('\t')
            aligned = align_g2p(word, transcr, self.g2p_map)

            for t in aligned:
                if t in extended_g2p_map:
                    extended_g2p_map[t] = extended_g2p_map[t] + 1
                else:
                    extended_g2p_map[t] = 1

        self.init_g2p_map(extended_g2p_map, min_occur)
        self.add_special_mappings()

    def add_special_mappings(self):
        if 'i' in self.g2p_map:
            self.g2p_map['y'] = self.g2p_map['i']
        if 'í' in self.g2p_map:
            self.g2p_map['ý'] = self.g2p_map['í']

        # ensure short and long versions of vowels
        for grapheme in self.g2p_map.keys():
            for p in self.g2p_map[grapheme]:
                if p in SHORT_VOWELS:
                    if p + ':' not in self.g2p_map[grapheme]:
                        self.g2p_map[grapheme].append(p + ':')
                elif p in LONG_VOWELS:
                    short = p.replace(':', '')
                    if short not in self.g2p_map[grapheme]:
                        self.g2p_map[grapheme].append(short)

        # manually add dipththongs and other special cases:
        self.g2p_map['ei'] = ['ei', 'ei:']
        self.g2p_map['ey'] = ['ei', 'ei:']
        self.g2p_map['au'] = ['9Y', '9Y:']
        self.g2p_map['hj'] = ['C']
        self.g2p_map['hl'] = ['l_0']
        self.g2p_map['hr'] = ['r_0']
        self.g2p_map['hn'] = ['n_0']
        self.g2p_map['sl'] = ['s t l']
        self.g2p_map['x'] = ['k s']
        self.g2p_map['é'] = ['j E', 'j E:']


def set_alignment(c, word_arr, tr_arr, g_anchor, p_anchor, g_ind, p_ind, g2p_tuples):
    graphemes = ''.join(word_arr[g_anchor + 1: g_ind])
    phonemes = ' '.join(tr_arr[p_anchor + 1: p_ind])
    if len(graphemes) > 0 or len(phonemes) > 0:
        g2p_tuples.append((graphemes, phonemes))
    g2p_tuples.append((c, tr_arr[p_ind]))
    if len(c) > 1:
        g_anchor = g_ind + 1
    else:
        g_anchor = g_ind
    p_anchor = p_ind
    return g_anchor, p_anchor, g2p_tuples


def set_triple_alignment(c, word_arr, tr_arr, g_anchor, p_anchor, g_ind, p_ind, g2p_tuples):
    graphemes = ''.join(word_arr[g_anchor + 1: g_ind])
    phonemes = ' '.join(tr_arr[p_anchor + 1: p_ind])
    if len(graphemes) > 0 or len(phonemes) > 0:
        g2p_tuples.append((graphemes, phonemes))
    g2p_tuples.append((c, ' '.join(tr_arr[p_ind: p_ind + 3])))

    g_anchor = g_ind + 1
    p_anchor = p_ind + 2
    return g_anchor, p_anchor, g2p_tuples


def set_two_phone_alignment(c, word_arr, tr_arr, g_anchor, p_anchor, g_ind, p_ind, g2p_tuples):
    graphemes = ''.join(word_arr[g_anchor + 1: g_ind])
    phonemes = ' '.join(tr_arr[p_anchor + 1: p_ind])
    if len(graphemes) > 0 or len(phonemes) > 0:
        g2p_tuples.append((graphemes, phonemes))
    g2p_tuples.append((c, ' '.join(tr_arr[p_ind: p_ind + 2])))

    g_anchor = g_ind
    p_anchor = p_ind + 1
    return g_anchor, p_anchor, g2p_tuples


def get_diphthong(ind, w_arr):
    diphthongs = ['ei', 'ey', 'au', 'hj', 'hl', 'hr', 'sl']
    if ind < len(w_arr) - 1:
        pair = w_arr[ind] + w_arr[ind+1]
        if pair.lower() in diphthongs:
            return pair.lower()

    return ''


def align_g2p(word, transcript, g2p_map):

    word_arr = list(word)
    tr_arr = transcript.split()

    g2p_tuples = []
    g_anchor = -1
    p_anchor = -1
    p_ind = 0
    skip_next = False
    for g_ind, c in enumerate(word_arr):
        if skip_next:
            skip_next = False
            continue
        c = c.lower()
        if p_ind < len(tr_arr) and c in g2p_map:
            if c == 'x' or c == 'é':
                tmp_phones = ' '.join(tr_arr[p_ind:p_ind + 2])
                if tmp_phones in g2p_map[c]:
                    g_anchor, p_anchor, g2p_tuples = set_two_phone_alignment(c, word_arr, tr_arr,
                                                                   g_anchor, p_anchor, g_ind, p_ind, g2p_tuples)
                    p_ind += 2
                    continue

            diph = get_diphthong(g_ind, word_arr)
            if len(diph) > 0:
                c = diph
                skip_next = True

            if c == 'sl':
                tmp_phones = ' '.join(tr_arr[p_ind:p_ind + 3])
                if tmp_phones == 's t l':
                    g_anchor, p_anchor, g2p_tuples = set_triple_alignment(c, word_arr, tr_arr,
                                                               g_anchor, p_anchor, g_ind, p_ind, g2p_tuples)
                    p_ind += 3

            if tr_arr[p_ind] in g2p_map[c]:
                g_anchor, p_anchor, g2p_tuples = set_alignment(c, word_arr, tr_arr,
                                                               g_anchor, p_anchor, g_ind, p_ind, g2p_tuples)
                p_ind += 1
            elif p_ind + 1 < len(tr_arr) and tr_arr[p_ind + 1] in g2p_map[c]:

                if g_ind < len(word_arr) - 1 and word_arr[g_ind + 1] in g2p_map and tr_arr[p_ind] in g2p_map[word_arr[g_ind + 1]]:
                    continue
                p_ind += 1
                g_anchor, p_anchor, g2p_tuples = set_alignment(c, word_arr, tr_arr,
                                                               g_anchor, p_anchor, g_ind, p_ind, g2p_tuples)
                p_ind += 1

            elif g_ind > p_ind:
                # if we have more phonemes left than graphemes, do not try to match ahead
                if len(word_arr) - g_ind > len(tr_arr) - p_ind:
                    continue
                if g_ind < len(tr_arr) and tr_arr[g_ind] in g2p_map[c]:
                    p_ind = g_ind
                    g_anchor, p_anchor, g2p_tuples = set_alignment(c, word_arr, tr_arr,
                                                                   g_anchor, p_anchor, g_ind, p_ind, g2p_tuples)
                    p_ind += 1
                elif g_ind + 1 < len(tr_arr) and tr_arr[g_ind + 1] in g2p_map[c]:
                    p_ind = g_ind + 1
                    g_anchor, p_anchor, g2p_tuples = set_alignment(c, word_arr, tr_arr,
                                                                   g_anchor, p_anchor, g_ind, p_ind, g2p_tuples)
                    p_ind += 1
            # last grapheme?
            elif g_ind == len(word_arr) - 1:
                graphemes = ''.join(word_arr[g_anchor + 1:])
                phonemes = ' '.join(tr_arr[p_anchor + 1:])
                g2p_tuples.append((graphemes, phonemes))
                break

        elif g_ind < len(tr_arr):
            p_ind += 1

        else:
            #check the end if p_anchor is not at the end of tr_arr
            if p_anchor < len(tr_arr) - 1:
                last_char = word_arr[-1]
                if last_char in g2p_map and tr_arr[-1] in g2p_map[last_char]:
                    graphemes = ''.join(word_arr[g_anchor + 1:-1])
                    phonemes = ' '.join(tr_arr[p_anchor + 1:-1])
                    if len(graphemes) > 0 or len(phonemes) > 0:
                        g2p_tuples.append((graphemes, phonemes))
                    g2p_tuples.append((last_char, tr_arr[-1]))
                    break

            graphemes = ''.join(word_arr[g_anchor + 1:])
            phonemes = ' '.join(tr_arr[p_anchor + 1:])
            g2p_tuples.append((graphemes, phonemes))
            break

    if g_anchor < len(word_arr) - 1 or p_anchor < len(tr_arr) - 1:
        graphemes = ''.join(word_arr[g_anchor + 1:])
        phonemes = ' '.join(tr_arr[p_anchor + 1:])
        g2p_tuples.append((graphemes, phonemes))
    return g2p_tuples


def main():

    pron_dict_in = open(sys.argv[1]).readlines()
    g2p = G2P_align(pron_dict_in, 1000)
    g2p.extend_mapping(pron_dict_in)

    tmp_g2p_map = {}
    g2p_map_v2 = {}
    aligned_dict = []
    for line in pron_dict_in:
        word, transcr = line.strip().split('\t')
        aligned = align_g2p(word, transcr, g2p.g2p_map)

        for t in aligned:
            if t in tmp_g2p_map:
                tmp_g2p_map[t].append(word + '  ---  ' + transcr)
            else:
                tmp_g2p_map[t] = [word + '  ---  ' + transcr]

            if t in g2p_map_v2:
                g2p_map_v2[t] = g2p_map_v2[t] + 1
            else:
                g2p_map_v2[t] = 1

        aligned_dict.append(word + '\t' + transcr + '\t' + str(aligned))

    for al in aligned_dict:
       print(str(al))

    out = open('alignment_map_train_v2.txt', 'w')
    for word in sorted(tmp_g2p_map, key=lambda x: len(tmp_g2p_map[x]), reverse=True):
        out.write(
            str(word) + '\t' + str(len(tmp_g2p_map[word])) + '\n')
        #if len(tmp_g2p_map[diff]) < 20:
        #    print(str(diff) + '\t' + str(tmp_g2p_map[diff]))
        #if len(diff[1]) == 0 and len(tmp_g2p_map[diff]) < 100:
        #    print(str(diff) + '\t' + str(tmp_g2p_map[diff]))


if __name__ == '__main__':
    main()