import unittest

from pron_dict_quality_assurance import grapheme_phoneme_mapping


class TestGraphemePhonemeMapping(unittest.TestCase):

    def test_align_g2p(self):
        g2p_map = self._get_g2p_map()
        word = 'aska'
        transcr = 'a s k a'
        res = grapheme_phoneme_mapping.align_g2p(word, transcr, g2p_map)
        self.assertEqual([('a', 'a'), ('s', 's'), ('k', 'k'), ('a', 'a')], res)

    def test_more_phones(self):
        g2p_map = self._get_g2p_map()
        word = 'séu'
        transcr = 's j E: Y'
        res = grapheme_phoneme_mapping.align_g2p(word, transcr, g2p_map)
        self.assertEqual([('s', 's'), ('é', 'j E:'), ('u', 'Y')], res)

    def test_less_phones(self):
        g2p_map = self._get_g2p_map()
        word = 'singdi'
        transcr = 's I N t I'
        res = grapheme_phoneme_mapping.align_g2p(word, transcr, g2p_map)
        self.assertEqual([('s', 's'), ('i', 'I'), ('n', 'N'), ('g', ''), ('d', 't'), ('i', 'I')], res)

    def test_abbadis(self):
        g2p_map = self._get_g2p_map()
        word = 'abbadísin'
        transcr = 'a p a t i: s I n'
        res = grapheme_phoneme_mapping.align_g2p(word, transcr, g2p_map)
        self.assertEqual(
            [('a', 'a'), ('b', 'p'), ('b', ''), ('a', 'a'), ('d', 't'), ('í', 'i:'), ('s', 's'), ('i', 'I'), ('n', 'n')], res)


    def test_adgangshardir(self):
        g2p_map = self._get_g2p_map()
        word = 'aðgangsharðir'
        transcr = 'a D k au N s h a r D I r'
        res = grapheme_phoneme_mapping.align_g2p(word, transcr, g2p_map)
        self.assertEqual(
            [('a', 'a'), ('ð', 'D'), ('g', 'k'), ('a', 'au'), ('n', 'N'), ('g', ''), ('s', 's'), ('h', 'h'), ('a', 'a'),
             ('r', 'r'), ('ð', 'D'), ('i', 'I'), ('r', 'r')], res
        )

    def test_lægstur(self):
        g2p_map = self._get_g2p_map()
        word = 'lægstur'
        transcr = 'l ai x s t Y r'
        res = grapheme_phoneme_mapping.align_g2p(word, transcr, g2p_map)
        self.assertEqual([('l', 'l'), ('æ', 'ai'), ('g', 'x'), ('s', 's'), ('t', 't'), ('u', 'Y'), ('r', 'r')], res)


    def test_mottokustod(self):
        g2p_map = self._get_g2p_map()
        word = 'móttökustöð'
        transcr = 'm ou: t 9 k Y s t 9: D'
        res = grapheme_phoneme_mapping.align_g2p(word, transcr, g2p_map)
        print(str(res))

    def test_myvatnssveit(self):
        g2p_map = self._get_g2p_map()
        word = 'Mývatnssveit'
        transcr = 'm i: v a s v ei: t'
        res = grapheme_phoneme_mapping.align_g2p(word, transcr, g2p_map)
        print(str(res))

    def test_motmaelti(self):
        g2p_map = self._get_g2p_map()
        word = 'mótmælti'
        transcr = 'm ou: t m ai l_0 t I'
        res = grapheme_phoneme_mapping.align_g2p(word, transcr, g2p_map)
        print(str(res))

    def test_motsogn(self):
        g2p_map = self._get_g2p_map()
        word = 'mótsögn'
        transcr = 'm ou: t s 9 k n_0'
        res = grapheme_phoneme_mapping.align_g2p(word, transcr, g2p_map)
        print(str(res))

    def test_einhverjar(self):
        g2p_map = self._get_g2p_map()
        word = 'einhverjar'
        transcr = 'ei N_0 k v E r j a r'
        res = grapheme_phoneme_mapping.align_g2p(word, transcr, g2p_map)
        self.assertEqual([('ei', 'ei'), ('n', 'N_0'), ('h', 'k'), ('v', 'v'), ('e', 'E'), ('r', 'r'), ('j', 'j'), ('a', 'a'), ('r', 'r')], res)

    def test_unglingsstulka(self):
        g2p_map = self._get_g2p_map()
        word = 'unglingsstúlka'
        transcr = 'u N l i N s t u l_0 k a'
        res = grapheme_phoneme_mapping.align_g2p(word, transcr, g2p_map)
        print(str(res))

    def test_adskotahlutur(self):
        g2p_map = self._get_g2p_map()
        word = 'aðskotahlutur'
        transcr = 'a D s k O t a l_0 Y: t Y r'
        res = grapheme_phoneme_mapping.align_g2p(word, transcr, g2p_map)
        self.assertEqual([('a', 'a'), ('ð', 'D'), ('s', 's'), ('k', 'k'), ('o', 'O'), ('t', 't'), ('a', 'a'), ('hl', 'l_0'), ('u', 'Y:'),
         ('t', 't'), ('u', 'Y'), ('r', 'r')], res)


    def test_kaupfelag(self):
        g2p_map = self._get_g2p_map()
        word = 'kaupfélags'
        transcr = 'k_h 9Y f j E l a x s'
        res = grapheme_phoneme_mapping.align_g2p(word, transcr, g2p_map)
        print(str(res))

    def test_kaupmanninum(self):
        g2p_map = self._get_g2p_map()
        word = 'kaupmanninum'
        transcr = 'k_h 9Y p m a n I n Y m'
        res = grapheme_phoneme_mapping.align_g2p(word, transcr, g2p_map)
        print(str(res))

    def test_fyrirgangi(self):
        g2p_map = self._get_g2p_map()
        word = 'fyrirgangi'
        transcr = 'f I: r I r k au J c I'
        res = grapheme_phoneme_mapping.align_g2p(word, transcr, g2p_map)
        print(str(res))

    def test_bandarikjathings(self):
        g2p_map = self._get_g2p_map()
        word = 'Bandaríkjaþings'
        transcr = 'p a n t a r i c a T i N k s'
        res = grapheme_phoneme_mapping.align_g2p(word, transcr, g2p_map)
        self.assertEqual([('b', 'p'), ('a', 'a'), ('n', 'n'), ('d', 't'), ('a', 'a'), ('r', 'r'), ('í', 'i'),
                         ('k', 'c'), ('j', ''), ('a', 'a'), ('þ', 'T'), ('i', 'i'), ('n', 'N'), ('g', 'k'), ('s', 's')], res)

    def test_hringdirdu(self):
        g2p_map = self._get_g2p_map()
        word = 'hringdirðu'
        transcr = 'r_0 i N t I r Y'
        res = grapheme_phoneme_mapping.align_g2p(word, transcr, g2p_map)
        print(str(res))

    def test_skornir(self):
        g2p_map = self._get_g2p_map()
        word = 'skornir'
        transcr = 's k O r t n I r'
        res = grapheme_phoneme_mapping.align_g2p(word, transcr, g2p_map)
        print(str(res))

    def test_adalsteinn(self):
        g2p_map = self._get_g2p_map()
        word = 'Aðalsteinn'
        transcr = 'a: D a l s t ei t n_0'
        res = grapheme_phoneme_mapping.align_g2p(word, transcr, g2p_map)
        self.assertEqual(
            [('a', 'a:'), ('ð', 'D'), ('a', 'a'), ('l', 'l'), ('s', 's'), ('t', 't'), ('ei', 'ei'), ('nn', 't n_0')], res)

    def test_hjonunum(self):
        g2p_map = self._get_g2p_map()
        word = 'hjónunum'
        transcr = 'C ou: n O n Y m'
        res = grapheme_phoneme_mapping.align_g2p(word, transcr, g2p_map)
        print(str(res))

    def test_aflahlutdeilda(self):
        g2p_map = self._get_g2p_map()
        word = 'aflahlutdeilda'
        transcr = 'a p l a l_0 Y: t ei l t a'
        res = grapheme_phoneme_mapping.align_g2p(word, transcr, g2p_map)
        self.assertEqual([('a', 'a'), ('f', 'p'), ('l', 'l'), ('a', 'a'), ('hl', 'l_0'), ('u', 'Y:'),
                          ('t', 't'), ('d', ''), ('ei', 'ei'), ('l', 'l'), ('d', 't'), ('a', 'a')], res)


    def test_krabbameinsfel(self):
        g2p_map = self._get_g2p_map()
        word = 'krabbameinsfélagsins'
        transcr = 'k_h r a p a m ei n s f j E: l a G s I n s'
        res = grapheme_phoneme_mapping.align_g2p(word, transcr, g2p_map)
        self.assertEqual([('k', 'k_h'), ('r', 'r'), ('a', 'a'), ('b', 'p'), ('b', ''), ('a', 'a'), ('m', 'm'),
                          ('ei', 'ei'), ('n', 'n'), ('s', 's'), ('f', 'f'), ('é', 'j E:'), ('l', 'l'), ('a', 'a'),
                          ('g', 'G'), ('s', 's'), ('i', 'I'), ('n', 'n'), ('s', 's')], res)


    def test_buxnavasanum(self):
        g2p_map = self._get_g2p_map()
        word = 'buxnavasanum'
        transcr = 'b Y k s t n a v a: s a n Y m'
        res = grapheme_phoneme_mapping.align_g2p(word, transcr, g2p_map)
        self.assertEqual([('b', 'b'), ('u', 'Y'), ('x', 'k s'), ('', 't'), ('n', 'n'), ('a', 'a'), ('v', 'v'),
                          ('a', 'a:'), ('s', 's'), ('a', 'a'), ('n', 'n'), ('u', 'Y'), ('m', 'm')], res)


    def test_areynslulaust(self):
        g2p_map = self._get_g2p_map()
        word = 'áreynslulaust'
        transcr = 'au: r ei n s t l Y l 9Y s t'
        res = grapheme_phoneme_mapping.align_g2p(word, transcr, g2p_map)
        print(str(res))

    def test_vatnsglas(self):
        g2p_map = self._get_g2p_map()
        word = 'vatnsglas'
        transcr = 'v a s k l a s'
        res = grapheme_phoneme_mapping.align_g2p(word, transcr, g2p_map)
        print(str(res))


    def _get_g2p_map(self):
        g2p = {'a': ['a', 'a:'],
               'æ': ['ai', 'ai:'],
               's': ['s'],
               'k': ['k_h', 'k', 'c'],
               'ð': ['D'], 'í': ['i', 'i:'],
               'r': ['r', 'r_0'],
               'm': ['m'],
               'd': ['t'],
               'v': ['v'],
               'á': ['au', 'au:'],
               'n': ['n', 'N'],
               'i': ['I', 'I:', 'i', 'i:'],
               'b':['p'],
               'o': ['O', 'O:'],
               'h': ['h', 'k'],
               'j': ['j'],
               'g': ['k', 'G', 'c'],
               'f': ['f', 'v'],
               'ó': ['ou:', 'ou'],
               't': ['t', 't_h', 'h'],
               'ö': ['9', '9:'],
               'l': ['l','t'],
               'u': ['Y', 'Y:'],
               'p': ['p'],
               'e': ['E:', 'E'],
               'ú': ['u', 'u:'],
               'þ': ['T'],
               'í': ['i', 'i:'],
               'y': ['I', 'I:', 'i', 'i:'],
               'ei': ['ei', 'ei:'],
               'ey': ['ei', 'ei:'],
               'au': ['9Y', '9Y:'],
               'hj' : ['C'],
                'hl' : ['l_0'],
                'hr' : ['r_0'],
               'é': ['j E', 'j E:'],
               'x' : ['k s'],
               'sl': ['s t l'],
               'tns': ['s']

               }

        return g2p
