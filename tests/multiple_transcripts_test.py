import unittest

from pron_dict_quality_assurance import multiple_transcripts


class TestMultipleTranscripts(unittest.TestCase):

    def test_compare_transcripts_same_len(self):
        transcr1 = 'aː t ɔ l f s ɔː n'
        transcr2 = 'aː t ou l f s ɔː n'

        self.assertEqual([('ɔ', 'ou')], multiple_transcripts.compare_transcripts(transcr1, transcr2))

    def test_compare_transcripts_diff_len(self):
        transcr1 = 'c ɛ t l i ŋ k'
        transcr2 = 'c ɛ r t l i ŋ k'

        self.assertEqual([('r', '')], multiple_transcripts.compare_transcripts(transcr1, transcr2))

        transcr1 = 'a v s k r ɪ f t a r ei h k n i ŋ k'
        transcr2 = 'a v s k r ɪ f t a r ei x n i ŋ k'

        self.assertEqual([('h k', 'x')], multiple_transcripts.compare_transcripts(transcr1, transcr2))

        transcr1 = 'p ɛ s a s t a ð a r̥ ɛ f s'
        transcr2 = 'p ɛ s a s t a ð a r̥ ɛ h p s'

        self.assertEqual([('h p', 'f')], multiple_transcripts.compare_transcripts(transcr1, transcr2))

        transcr1 = 'p ɛ r n h a r ð s ɔː n'
        transcr2 = 'p ɛ r n h a r ð s ɔː n a r'

        self.assertEqual([('a r', '')], multiple_transcripts.compare_transcripts(transcr1, transcr2))

        transcr1 = 'a ð v ɛ n̥ t ʏ k v œ l t'
        transcr2 = 'a ð v ɛ n t ʏ k v œ l t'

        self.assertEqual([('n̥', 'n')], multiple_transcripts.compare_transcripts(transcr1, transcr2))

        transcr1 = 'c ɛ t l i ŋ k'
        transcr2 = 'c ɛ r t l i ŋ k'

        self.assertEqual([('r', '')], multiple_transcripts.compare_transcripts(transcr1, transcr2))


    def test_compare_transcript_multi_diff(self):
        transcr1 = 'f ɛː l ɪ k s ɔː n'
        transcr2 = 'f ɛː l i k s ɔ n'

        self.assertEqual([('ɪ', 'i'), ('ɔː', 'ɔ')], multiple_transcripts.compare_transcripts(transcr1, transcr2))

    def test_transcript_diff(self):
        arr = ['Felixson\tf ɛː l ɪ k s ɔː n', 'Felixson\tf ɛː l i k s ɔ n', 'Felixson\tf ɛː l ɪ x s ɔː n']

        self.assertEqual([('ɪ', 'i'), ('ɔː', 'ɔ'), ('k', 'x')], multiple_transcripts.transcript_diff(arr))

    def test_additional_cases(self):

        arr = ['Reykjavíkurvegi\tr eiː k j a v iː k ʏ r v eiː j ɪ',
                'Reykjavíkurvegi\tr eiː c a v i k ʏ r v ei j ɪ']

        self.assertEqual([('k j', 'c'), ('iː', 'i'), ('eiː', 'ei')], multiple_transcripts.transcript_diff(arr))

        arr = ['Gestsson\tc ɛ s t s ɔː n', 'Gestsson\tc ɛ s t s ɔ n', 'Gestsson\tc ɛ s ɔ n']
        self.assertEqual([('ɔː', 'ɔ'), ('t s ɔː', 'ɔ')], multiple_transcripts.transcript_diff(arr))

    def test_empty_tuple_error(self):
        transcr1 = 's v ɛ p n v aː n a'
        transcr2 = 's v ɛ p v a n a'

        self.assertEqual([('n', ''), ('aː', 'a')], multiple_transcripts.compare_transcripts(transcr1, transcr2))

        transcr1 = 's ɛ ð l a p au ɲ̊ c ɪ ɪ'
        transcr2 = 's ɛ ð l a p au ɲ c ɪ'

        self.assertEqual([('ɲ̊', 'ɲ'), ('ɪ', '')], multiple_transcripts.compare_transcripts(transcr1, transcr2))

        transcr1 = 'f ɪː r ɪ r l ɪː ð ɪ n'
        transcr2 = 'f ɪː r ɪ l ɪ ð ɪ n'

        self.assertEqual([('r', ''), ('ɪː', 'ɪ')], multiple_transcripts.compare_transcripts(transcr1, transcr2))

        transcr1 = 'k aː p r i j ɛ l a'
        transcr2 = 'k a p r i ɛ l a'

        self.assertEqual([('aː', 'a'), ('j', '')], multiple_transcripts.compare_transcripts(transcr1, transcr2))

        transcr1 = 'l ai h k n a f j ɛː l a x s'
        transcr2 = 'l ai x n a f j ɛː l a x s'

        self.assertEqual([('h k', 'x')], multiple_transcripts.compare_transcripts(transcr1, transcr2))

        transcr1 = 'n ɔ r ð l i ŋ k a h ɔ l̥ t ɪ'
        transcr2 = 'n ɔ r l ɪ ɲ k a h ɔ l̥ t ɪ'

        self.assertEqual([('ð', ''), ('i ŋ', 'ɪ ɲ')], multiple_transcripts.compare_transcripts(transcr1, transcr2))


    def test_choose_transcript(self):

        chosen_transcript = multiple_transcripts.choose_transcript([('bla', 'blubb')], 'transcr1', 'transcr2', 'word')
        print(chosen_transcript)

        chosen_transcript = multiple_transcripts.choose_transcript([], 'aː ð a l ei ŋ̊ k ʏ n', 'aː ð a l ei ŋ̊ k ʏ n', 'aðaleinkunn')
        print(chosen_transcript)

