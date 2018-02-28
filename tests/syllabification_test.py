# -*- coding: utf-8 -*-

import unittest

from pron_dict import entry
from pron_dict import syllabification
from pron_dict import stress


class TestSyllabification(unittest.TestCase):

    def test_syllab_dict(self):
        test_dict = self._get_test_dict1()
        syllab = syllabification.syllabify_dict(test_dict)

        for entry in syllab:
            if entry.word == 'skrautskrift':
                res_syllables = []
                for syll in entry.syllables:
                    res_syllables.append(syll.content)
                self.assertEqual('s k r 9Y: t s k r I f t', entry.transcript)
                self.assertEqual(['s k r 9Y: t ', 's k r I f t '], res_syllables)

    """
    def test_stress(self):
        test_dict = self._get_test_dict1()
        syllab = syllabification.syllabify_dict(test_dict)
        syllab_with_stress = stress.set_stress(syllab)
        for entry in syllab_with_stress:
            if entry.word == 'skrautskrift':
                print(entry)
                self.assertEqual(['s k r 9Y: t', 's k r I f t'], entry.syllables)

    """

    @unittest.skip("skip single syllab")
    def test_single_syllab(self):
        elem = entry.PronDictEntry('strandríki', 's t r a n t r i c ɪ')
        syllab = syllabification.syllabify(elem)
        self.assertEqual(['s t r a n t', 'r i c I'], syllab.syllables)

        elem = entry.PronDictEntry('strandríkja', 's t r a n t r i c a')
        syllab = syllabification.syllabify(elem)
        self.assertEqual(['s t r a n t', 'r i c a'], syllab.syllables)

        elem = entry.PronDictEntry('strangtrúaðir', 's t r au: N k t r u a D I r')
        syllab = syllabification.syllabify(elem)
        self.assertEqual(['s t r au: N k', 't r u a D I r'], syllab.syllables)

        elem = entry.PronDictEntry('strangtrúaðra', 's t r au: N k t r u a D r a')
        syllab = syllabification.syllabify(elem)
        self.assertEqual(['s t r au: N k', 't r u a D r a'], syllab.syllables)

    def test_je_syllables(self):

        elem = entry.PronDictEntry('víetnamstríðinu', 'v i j E h t n a m s t r i: D I n Y')
        syllab = syllabification.syllabify(elem)
        res_syllables = []
        for syll in syllab.syllables:
            res_syllables.append(syll.content)

        self.assertEqual(['v i ', 'j E h t ', 'n a m ', 's t r i: ', 'D I ', 'n Y '], res_syllables)


    @unittest.skip('skip compound')
    def test_compound_analysis(self):
        elem = entry.PronDictEntry('ljósvakamiðlar')
        syllabification.syllabify_on_subwords(elem)


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
