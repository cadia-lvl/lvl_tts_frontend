#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class PronDictEntry:
    """
    Contains information on a pronunciation dict entry and methods to manipulate it

    The initialisation of a PronDictEntry object takes a word string and its transcription as parameters.
    """

    def __init__(self, word='', transcription=''):
        """

        :param word: a dictionary entry (ex: 'dag')
        :param transcription: transcription of 'word', with the phones space separated (ex: 't a: G')

        """
        self.word = word
        self.transcript = transcription.strip()
        self.transcription_arr = self.transcript.split()
        self.gpos = 'nil'  # guessed part-of-speech
        self.syllables = []
        self.head = ''
        self.modifier = ''
        self.full_decomp = ''

    def __str__(self):
        return self.word + '\t' + self.gpos + '\t' + self.transcript + '\t' + str(self.syllables)

    def __repr__(self):
        return self.__str__()

    def update_syllables(self, ind, prev_syll, syll):
        self.syllables[ind - 1] = prev_syll
        self.syllables[ind] = syll

    def format_syllables(self):
        formatted_string = '('
        for syll in self.syllables:
            formatted_string += '((' + syll.content + ') ' + str(syll.stress) + ') '

        return formatted_string.strip() + ')'

    def cmu_format(self):
        return '("' + self.word + '" ' + self.gpos + ' ' + self.format_syllables() + ')'