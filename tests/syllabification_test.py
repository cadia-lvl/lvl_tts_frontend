# -*- coding: utf-8 -*-

import unittest

from pron_dict import entry
from pron_dict import syllabification
from pron_dict import tree_builder
from pron_dict import stress


class TestSyllabification(unittest.TestCase):

    def get_syllable_arr(self, syllables):
        syllable_arr = []
        for syll in syllables:
            syllable_arr.append(syll.content)

        return syllable_arr


    def test_single_syllab(self):

        comp_tree = tree_builder.build_compound_tree(
            entry.PronDictEntry('strandríki', 's t r a n t r i c I'))
        syllables = []
        syllabification.syllabify_tree(comp_tree, syllables)
        res_syllables = self.get_syllable_arr(syllables)
        self.assertEqual(['s t r a n t ', 'r i ', 'c I '], res_syllables)

        comp_tree = tree_builder.build_compound_tree(entry.PronDictEntry('strandríkja', 's t r a n t r i c a'))
        syllables = []
        syllabification.syllabify_tree(comp_tree, syllables)
        res_syllables = self.get_syllable_arr(syllables)
        self.assertEqual(['s t r a n t ', 'r i ', 'c a '], res_syllables)

        comp_tree = tree_builder.build_compound_tree(
            entry.PronDictEntry('strangtrúaðir', 's t r au: N k t r u a D I r'))
        syllables = []
        syllabification.syllabify_tree(comp_tree, syllables)
        res_syllables = self.get_syllable_arr(syllables)
        self.assertEqual(['s t r au: N k ', 't r u ', 'a ', 'D I r '], res_syllables)

        comp_tree = tree_builder.build_compound_tree(
            entry.PronDictEntry('strangtrúaðra', 's t r au: N k t r u a D r a'))
        syllables = []
        syllabification.syllabify_tree(comp_tree, syllables)
        res_syllables = self.get_syllable_arr(syllables)
        self.assertEqual(['s t r au: N k ', 't r u ', 'a D ', 'r a '], res_syllables)

    def test_je_syllables(self):

        comp_tree = tree_builder.build_compound_tree(
            entry.PronDictEntry('víetnamstríðinu', 'v i j E h t n a m s t r i: D I n Y'))
        syllables = []
        syllabification.syllabify_tree(comp_tree, syllables)
        res_syllables = self.get_syllable_arr(syllables)

        self.assertEqual(['v i ', 'j E h t ', 'n a m ', 's t r i: ', 'D I ', 'n Y '], res_syllables)

    def test_compound_analysis(self):
        comp_tree = tree_builder.build_compound_tree(
            entry.PronDictEntry('ljósvakamiðlar', 'l j ou: s v a k a m I D l a r'))
        syllables = []
        syllabification.syllabify_tree(comp_tree, syllables)
        res_syllables = self.get_syllable_arr(syllables)

        self.assertEqual(['l j ou: s ', 'v a ', 'k a ', 'm I D ', 'l a r '], res_syllables)

        comp_tree = tree_builder.build_compound_tree(
            entry.PronDictEntry('afbragðsgott', 'a v p r a G s k O h t'))
        syllables = []
        syllabification.syllabify_tree(comp_tree, syllables)
        res_syllables = self.get_syllable_arr(syllables)

        self.assertEqual(['a v ', 'p r a G s ', 'k O h t '], res_syllables)

        comp_tree = tree_builder.build_compound_tree(
            entry.PronDictEntry('afmælisbarninu', 'a m ai l I s p a r t n I n Y'))
        syllables = []
        syllabification.syllabify_tree(comp_tree, syllables)
        res_syllables = self.get_syllable_arr(syllables)

        self.assertEqual(['a ', 'm ai ', 'l I s ', 'p a r t ', 'n I ', 'n Y '], res_syllables)

        comp_tree = tree_builder.build_compound_tree(
            entry.PronDictEntry('gjaldeyrisvarasjóð', 'c a l t ei r I s v a r a s j ou: D'))
        syllables = []
        syllabification.syllabify_tree(comp_tree, syllables)
        res_syllables = self.get_syllable_arr(syllables)

        # self.assertEqual(['c a l t ', 'ei ', 'r I s ', 'v a ', 'r a ', 's j ou: D '], res_syllables)

        comp_tree = tree_builder.build_compound_tree(
            entry.PronDictEntry('parkinsonssamtökin', 'p_h a r_0 c I n s O n s a m t 9 c I n'))
        syllables = []
        syllabification.syllabify_tree(comp_tree, syllables)
        res_syllables = self.get_syllable_arr(syllables)

        self.assertEqual(['p_h a r_0 ', 'c I n ', 's O n ', 's a m ', 't 9 ', 'c I n '], res_syllables)


    def _get_test_dict1(self):

        entry_dict = []
        entry_dict.append(entry.PronDictEntry('skratti', 's k r a h t I'))
        entry_dict.append(entry.PronDictEntry('skrattinn', 's k r a h t I n'))
        entry_dict.append(entry.PronDictEntry('skraut', 's k r 9Y: t'))
        entry_dict.append(entry.PronDictEntry('skrautfiska', 's k r 9Y: t f I s k a'))
        entry_dict.append(entry.PronDictEntry('skrautfjöður', 's k r 9Y: t f j 9 D Y r'))
        entry_dict.append(entry.PronDictEntry('skrauti', 's k r 9Y: t I'))
        entry_dict.append(entry.PronDictEntry('skrautinu', 's k r 9Y: t I n Y'))
        entry_dict.append(entry.PronDictEntry('skrautið', 's k r 9Y: t I D'))
        entry_dict.append(entry.PronDictEntry('skrautleg', 's k r 9Y: t l E G'))
        entry_dict.append(entry.PronDictEntry('skrautlega', 's k r 9Y: t l E G a'))
        entry_dict.append(entry.PronDictEntry('skrautlegan', 's k r 9Y: t l E G a n'))
        entry_dict.append(entry.PronDictEntry('skrautlegar', 's k r 9Y: t l E G a r'))
        entry_dict.append(entry.PronDictEntry('skrautlegasta', 's k r 9Y: t l E G a s t a'))
        entry_dict.append(entry.PronDictEntry('skrautlegir', 's k r 9Y: t l E j I r'))
        entry_dict.append(entry.PronDictEntry('skrautlegra', 's k r 9Y: t l E G r a'))
        entry_dict.append(entry.PronDictEntry('skrautlegri', 's k r 9Y: t l E G r I'))
        entry_dict.append(entry.PronDictEntry('skrautlegt', 's k r 9Y: t l E x t'))
        entry_dict.append(entry.PronDictEntry('skrautlegu', 's k r 9Y: t l E G Y'))
        entry_dict.append(entry.PronDictEntry('skrautlegum', 's k r 9Y: t l E G Y m'))
        entry_dict.append(entry.PronDictEntry('skrautlegur', 's k r 9Y: t l E G Y r'))
        entry_dict.append(entry.PronDictEntry('skrautmuni', 's k r 9Y: t m Y n I'))
        entry_dict.append(entry.PronDictEntry('skrautmunir', 's k r 9Y: t m Y n I r'))
        entry_dict.append(entry.PronDictEntry('skrautritun', 's k r 9Y: t r I t Y n'))
        entry_dict.append(entry.PronDictEntry('skrauts', 's k r 9Y: t s'))
        entry_dict.append(entry.PronDictEntry('skrautskrift', 's k r 9Y: t s k r I f t'))
        entry_dict.append(entry.PronDictEntry('skref', 's k r E: v'))
        entry_dict.append(entry.PronDictEntry('skrefa', 's k r E: v a'))

        return entry_dict
