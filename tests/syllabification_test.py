# -*- coding: utf-8 -*-

import unittest

from pron_dict import entry
from pron_dict import syllabification
from pron_dict import tree_builder


class TestSyllabification(unittest.TestCase):

    def get_syllable_arr(self, syllables):
        syllable_arr = []
        for syll in syllables:
            syllable_arr.append(syll.content)

        return syllable_arr


    def test_single_syllab(self):
        comp_tree = tree_builder.build_compound_tree(entry.PronDictEntry('baunaspírum', 'b 9Y: n a s p i: r Y m'))
        syllables = []
        syllabification.syllabify_tree(comp_tree, syllables)
        res_syllables = self.get_syllable_arr(syllables)
      #  self.assertEqual(['b 9Y: ', 'n a ', 's p i: ', 'r Y m '], res_syllables)

        comp_tree = tree_builder.build_compound_tree(entry.PronDictEntry('afturhvarf', 'a f t Y r k v a r v'))
        syllables = []
        syllabification.syllabify_tree(comp_tree, syllables)
        res_syllables = self.get_syllable_arr(syllables)
        self.assertEqual(['a f ', 't Y r ', 'k v a r v '], res_syllables)

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

        comp_tree = tree_builder.build_compound_tree(
            entry.PronDictEntry('aftanákeyrslu', 'a f t a n au c ei r_0 s t l Y'))
        syllables = []
        syllabification.syllabify_tree(comp_tree, syllables)
        res_syllables = self.get_syllable_arr(syllables)

        self.assertEqual(['a f ', 't a ', 'n au ', 'c ei r_0 s t ', 'l Y '], res_syllables)
