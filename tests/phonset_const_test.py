# -*- coding: utf-8 -*-

import unittest

from pron_dict_quality_assurance import phoneset_consistency


class TestPhonesetConsistency(unittest.TestCase):

    def test_replace_phonemes(self):
        res, repl = phoneset_consistency.correct_transcript('alcɛj\u014b\u0325t')
        self.assertEqual('alcɛj\u014b\u030at', res)

        res, repl = phoneset_consistency.correct_transcript('fi\u014b\u0325kʏr')
        self.assertEqual('fi\u014b\u030akʏr', res)

        res, repl = phoneset_consistency.correct_transcript('abl̥stirɪ')
        self.assertEqual('apl̥stirɪ', res)

        res, repl = phoneset_consistency.correct_transcript('uŋk̥tʰɛm̥plarar')
        self.assertEqual('uŋktʰɛm̥plarar', res)

    def test_remove_symbols(self):
        res, repl = phoneset_consistency.correct_transcript('pɔrðstɔvʏ///')
        self.assertEqual('pɔrðstɔvʏ', res)

    def test_correct_length_symbols(self):
        res = phoneset_consistency.correct_diphthongs('auːratʏiːjɪ')
        self.assertEqual('auːratʏijɪ', res)

        res = phoneset_consistency.correct_diphthongs('pɔiːjɪ')
        self.assertEqual('pɔijɪ', res)

        res, repl = phoneset_consistency.correct_transcript('peinːhœrðʏm')
        self.assertEqual('peinhœrðʏm', res)

        res, repl = phoneset_consistency.correct_transcript('tjupːʏvik')
        self.assertEqual('tjupʏvik', res)

        res, repl = phoneset_consistency.correct_transcript('fɪlcɪrɪtː')
        self.assertEqual('fɪlcɪrɪt', res)

        res, repl = phoneset_consistency.correct_transcript('laiːː')
        self.assertEqual('laiː', res)





