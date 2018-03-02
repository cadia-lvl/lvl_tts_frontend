#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
The pron_dict module processes an ASR pronunciation dictionary, containing entries of the form 'word     transcription',
computes the necessary additional information for TTS (part-of-speech, syllabification and stress marks) and
outputs the results in the Festvox format.

Example:
    Input entry:

    adolfsdóttir     a: t O l f s t ou h d I r

    Output entry:

    ("adolfsdóttir" n (((a:) 1) ((t O l f s) 3) ((t ou h) 1) ((d I r) 3))))


"""

"""
# TODO:

0) Fork Ossian, keep in sync, branch to 'lvl' to make changes - document and make it easy to add new languages

1) wrong syllabification in words like 'daníel': ("daníel" nil (((t a: ) 1) ((n ) 0) ((i j E l ) 0))).
    Also: adíel, daníels, daníelsdóttir, daníelsdóttur, daníelsson, daníelssonar, daníelssyni, gabriel,
    gabríel, gabríels, gamalíel, gamalíelsson. víetnamstríðinu etc. 'íe' seems to be the problem, not only the
    'j' is moved, but also the preceeding 'i' (instead of vi-jEt-nam, we have v-ijEt-nam) 
    Also: ei j E like leigjenda -> l-eijEn-ta - or just all combinations vowel+é ? slydduél, fjallajeppa, flygenring ('flíeríng),
    viðhlæjendur, hýenur

2) Errors: check original frob. Original errors or errors caused by syllabification? Caused by syllabification, fixed.

("skrautskrift" n (((s ) 1) ((k r I f t ) 0)))                          frob: s k r œy t s k r ɪ f t / s k r 9Y t s k r I f t
("strandríki" n (((s ) 1) ((t r i ) 0) ((c I ) 0)))                     frob: s t r a n t r i c ɪ / s t r a n t r i c I
("strandríkja" n (((s ) 1) ((t r i ) 0) ((c a ) 0)))                    frob: s t r a n t r i c a / s t r a n t r i c a
("strandríkjanna" n (((s ) 1) ((t r i: ) 0) ((c a ) 0) ((n a ) 0)))     frob: s t r a n t r iː c a n a / s t r a n t r i: c a n a
("strangtrúaðir" j (((s ) 1) ((t r u ) 0) ((a ) 0) ((D I r ) 0)))       frob: s t r auː ŋ k t r u a ð ɪ r / s t r au: N k t r u a D I r
("strangtrúaðra" j (((s ) 1) ((t r u ) 0) ((a D ) 0) ((r a ) 0)))       frob: s t r auː ŋ k t r u a ð r a / s t r au: N k t r u a D r a
    
3) Sanity check: control each syllabified word and see if it does not definitely have a vowel

4) Double entries: DONE

("fleiri" j (((f l ei ) 1) ((r I ) 0)))
("fleiri" j (((f l ei: ) 1) ((r I ) 0)))

("björnsson" nil (((p j P r_0 ) 1) ((s O n ) 0)))
("björnsson" nil (((p j P ) 1) ((s O n ) 0)))

("björnssonar" nil (((p j P r_0 ) 1) ((s O ) 0) ((n a r ) 0)))
("björnssonar" nil (((p j P ) 1) ((s O ) 0) ((n a r ) 0)))

etc. ...

extract all double entries and decied on pronunciation

5) Compound analysis. Combine with syllabification, insert the resulting algorithm into Ossian. Before
"messing" with Ossian: fork project from github.

5) Test quality of g2p. How large should the training set be? Current (Ossian default): 1000 entries.
    
"""

__license__ = 'Apache 2.0 (see: LICENSE)'

import argparse
import gpos
import syllabification
import stress
import tree_builder


from entry import PronDictEntry


def init_pron_dict(dict_file):
    pron_dict = []
    for line in dict_file:
        word, transcr = line.split('\t')
        entry = PronDictEntry(word, transcr)
        pron_dict.append(entry)
    return pron_dict


def create_tree_list(pron_dict):

    tree_list = []
    for entry in pron_dict:
        t = tree_builder.build_compound_tree(entry)
        tree_list.append(t)
    return tree_list


def parse_args():
    parser = argparse.ArgumentParser(description='pronunciation dictionary for TTS', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('i', type=argparse.FileType('r'), help='ASR pronunciation dictionary')
   # parser.add_argument('o', type=argparse.FileType('w'), default='', help='Output: TTS pronunciation dictionary')

    return parser.parse_args()


def main():

    args = parse_args()
    pron_dict = init_pron_dict(args.i)
    gpos.perform_gpos_for_entry_list(pron_dict)

    tree_dict = create_tree_list(pron_dict)

    syllabified = syllabification.syllabify_dict(tree_dict)
    syllab_with_stress = stress.set_stress(syllabified)
    #print('MNCL')
    #for entry in syllab_with_stress:
    #    print(entry.cmu_format())


if __name__ == '__main__':
    main()
