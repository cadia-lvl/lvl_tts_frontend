#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

SHORT_VOWELS = ['a', 'E', 'I', 'i', 'O', 'Y', 'u', '9', 'ai', 'ei', 'Ou', '9Y']
LONG_VOWELS = ['a:', 'E:', 'I:', 'i:', 'O:', 'Y:', 'u:', '9:', 'ai:', 'ei:', 'Ou:', '9Y:']

def map_g2p(word, transcript):
    word_arr = list(word)
    tr_arr = transcript.split()

    g2p_tuples = []
    if len(word_arr) != len(tr_arr):
        return g2p_tuples

    for ind, c in enumerate(word_arr):
        g2p_tuples.append((c.lower(), tr_arr[ind]))

    return g2p_tuples

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

    tmp_g2p_map = {}
    for line in pron_dict_in:
        word, transcr = line.strip().split('\t')

        result = map_g2p(word, transcr)
        #if len(result) == 0:
        #    print(line.strip())

        for t in result:
            if t in tmp_g2p_map:
                tmp_g2p_map[t] = tmp_g2p_map[t] + 1
            else:
                tmp_g2p_map[t] = 1

    g2p_map = {}
    for t in tmp_g2p_map.keys():
        if tmp_g2p_map[t] > 1000:
            if t[0] in g2p_map:
                g2p_map[t[0]].append(t[1])
            else:
                g2p_map[t[0]] = [t[1]]

    if 'i' in g2p_map:
        g2p_map['y'] = g2p_map['i']
    if 'í' in g2p_map:
        g2p_map['ý'] = g2p_map['í']

    # ensure short and long versions of vowels
    for grapheme in g2p_map.keys():
        for p in g2p_map[grapheme]:
            if p in SHORT_VOWELS:
                if p + ':' not in g2p_map[grapheme]:
                    g2p_map[grapheme].append(p + ':')
            elif p in LONG_VOWELS:
                short = p.replace(':','')
                if short not in g2p_map[grapheme]:
                    g2p_map[grapheme].append(short)


    #manually add dipththongs and h: k for 'hv':
    g2p_map['ei'] = ['ei', 'ei:']
    g2p_map['ey'] = ['ei', 'ei:']
    g2p_map['au'] = ['9Y', '9Y:']
    g2p_map['hj'] = ['C']
    g2p_map['hl'] = ['l_0']
    g2p_map['hr'] = ['r_0']
    g2p_map['hn'] = ['n_0']
    g2p_map['sl'] = ['s t l']

    tmp_g2p_map = {}
    g2p_map_v2 = {}
    aligned_dict = []
    for line in pron_dict_in:
        word, transcr = line.strip().split('\t')
        aligned = align_g2p(word, transcr, g2p_map)

        for t in aligned:
            if t in tmp_g2p_map:
                tmp_g2p_map[t].append(word + '  ---  ' + transcr)
                """
                if len(tmp_g2p_map[t]) > 100:
                    if t[0] in g2p_map:
                        g2p_map[t[0]].append(t[1])
                    else:
                        g2p_map[t[0]] = [t[1]]
                """

            else:
                tmp_g2p_map[t] = [word + '  ---  ' + transcr]

            if t in g2p_map_v2:
                g2p_map_v2[t] = g2p_map_v2[t] + 1
            else:
                g2p_map_v2[t] = 1


        aligned_dict.append(word + '\t' + transcr + '\t' + str(aligned))


    g2p_map = {}
    g2p_map['x'] = ['k s']
    g2p_map['é'] = ['j E', 'j E:']

    for t in g2p_map_v2.keys():
        if g2p_map_v2[t] > 100:
            if t[0] in g2p_map:
                g2p_map[t[0]].append(t[1])
            else:
                g2p_map[t[0]] = [t[1]]

    if 'i' in g2p_map:
        g2p_map['y'] = g2p_map['i']
    if 'í' in g2p_map:
        g2p_map['ý'] = g2p_map['í']

    # ensure short and long versions of vowels
    for grapheme in g2p_map.keys():
        for p in g2p_map[grapheme]:
            if p in SHORT_VOWELS:
                if p + ':' not in g2p_map[grapheme]:
                    g2p_map[grapheme].append(p + ':')
            elif p in LONG_VOWELS:
                short = p.replace(':', '')
                if short not in g2p_map[grapheme]:
                    g2p_map[grapheme].append(short)

    # manually add dipththongs and h: k for 'hv':
    g2p_map['ei'] = ['ei', 'ei:']
    g2p_map['ey'] = ['ei', 'ei:']
    g2p_map['au'] = ['9Y', '9Y:']
    g2p_map['hj'] = ['C']
    g2p_map['hl'] = ['l_0']
    g2p_map['hr'] = ['r_0']
    g2p_map['hn'] = ['n_0']
    g2p_map['sl'] = ['s t l']

    tmp_g2p_map = {}
    g2p_map_v2 = {}
    aligned_dict = []
    for line in pron_dict_in:
        word, transcr = line.strip().split('\t')
        aligned = align_g2p(word, transcr, g2p_map)

        for t in aligned:
            if t in tmp_g2p_map:
                tmp_g2p_map[t].append(word + '  ---  ' + transcr)
                """
                if len(tmp_g2p_map[t]) > 100:
                    if t[0] in g2p_map:
                        g2p_map[t[0]].append(t[1])
                    else:
                        g2p_map[t[0]] = [t[1]]
                """

            else:
                tmp_g2p_map[t] = [word + '  ---  ' + transcr]

            if t in g2p_map_v2:
                g2p_map_v2[t] = g2p_map_v2[t] + 1
            else:
                g2p_map_v2[t] = 1

        aligned_dict.append(word + '\t' + transcr + '\t' + str(aligned))


    for al in aligned_dict:
       print(str(al))

    out = open('alignment_map_train.txt', 'w')
    for diff in sorted(tmp_g2p_map, key=lambda x: len(tmp_g2p_map[x]), reverse=True):
        out.write(
            str(diff) + '\t' + str(len(tmp_g2p_map[diff])) + '\n')
        #if len(tmp_g2p_map[diff]) < 20:
        #    print(str(diff) + '\t' + str(tmp_g2p_map[diff]))
        #if len(diff[1]) == 0 and len(tmp_g2p_map[diff]) < 100:
        #    print(str(diff) + '\t' + str(tmp_g2p_map[diff]))




if __name__ == '__main__':
    main()