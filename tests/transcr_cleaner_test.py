# -*- coding: utf-8 -*-

import unittest

from sltu_experiments import transcr_cleaner

class TestTranscrCleaner(unittest.TestCase):

    def test_clean_stress_true(self):
        transcr = 'h a1 p  | n a0 r  | f j a1 r  | D a0 r  | c I1 r_0  | c Y0'
        clean = transcr_cleaner.clean_transcript(transcr, True)

        self.assertEqual('h a p n a r f j a r D a r c I r_0 c Y', clean)

        transcr = 's a1 m  | c_h I0 r_0  | c Y0  | l E:0  | G Y0'
        clean = transcr_cleaner.clean_transcript(transcr, True)

        self.assertEqual('s a m c_h I r_0 c Y l E: G Y', clean)


    def test_clean_stress_false(self):
        transcr = 'h a1 p  | n a0 r  | f j a1 r  | D a0 r  | c I1 r_0  | c Y0'
        clean = transcr_cleaner.clean_transcript(transcr, False)

        self.assertEqual('h a1 p n a0 r f j a1 r D a0 r c I1 r_0 c Y0', clean)

        transcr = 's a1 m  | c_h I0 r_0  | c Y0  | l E:0  | G Y0'
        clean = transcr_cleaner.clean_transcript(transcr, False)

        self.assertEqual('s a1 m c_h I0 r_0 c Y0 l E:0 G Y0', clean)
