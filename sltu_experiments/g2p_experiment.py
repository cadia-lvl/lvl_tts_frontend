#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test quality of automatic g2p using Sequitur.

1) Train a model using a selected training set (self.train_file). The training file is of the format:
    word w o r d

    no tab between word and transcription.

2) Test the model using an input test file, see main()
    When testing, the number of errors, the error rate and all errors with correct transcriptions are written
    to a result file.

Be careful to use the same sort of training and test data, i.e. with or without stress labels.

"""

import os
import shutil
import subprocess
import unicodedata
import re


class G2P_Experiment:

    def __init__(self):
        self.train_file = '/Users/anna/PycharmProjects/lvl_tts_frontend/sltu_experiments/data/g2p_train_1000_clean.txt'
        # set-up as in Ossian scripts/processors/Lexicon.py
        self.g2p_path = 'export PYTHONPATH=/Users/anna/Ossian/tools/bin/../lib/python2.7/site-packages:/Users/anna/Ossian/tools/bin/../g2p ;'
        self.lts_tool = '/Users/anna/Ossian/tools/bin/g2p.py'
        self.max_graphone_letters = 2
        self.max_graphone_phones = 2
        self.lts_gram_length = 3
        self.lts_fname = 'lts.model'
        self.lts_ntrain = 0 # train on all training input
        self.lts_model = ''

    def train_sequitur_g2p(self):

        lts_model = self.lts_fname
        print('Training LTS with sequitur...')
        ## train unigram model:
        n = 1
        comm = '%s %s --train %s -s 1,%s,1,%s --devel 5%% --encoding utf8 --write-model %s_%s > %s.log' % (self.g2p_path, self.lts_tool,
                                                                                                       self.train_file,
                                                                                                       self.max_graphone_letters, \
                                                                                                       self.max_graphone_phones,
                                                                                                       lts_model, n,
                                                                                                       lts_model)
        print(comm)
        os.system(comm)
        n += 1
        # train an ngram model according to self.lts_gram_length
        while n <= self.lts_gram_length:
            comm = '%s %s --model %s_%s --ramp-up --train %s --devel 5%% --encoding utf8 --write-model %s_%s >> %s.log' % (
                self.g2p_path, self.lts_tool, lts_model, n - 1, self.train_file, lts_model, n, lts_model)
            print(comm)
            os.system(comm)
            n += 1
        shutil.copy('%s_%s' % (lts_model, self.lts_gram_length), lts_model)
        self.lts_model = lts_model

    def get_oov_pronunciation(self, word):

        escaped_word = "'" + word.lower() + "'"

        comm = '%s echo %s | %s  --model %s --encoding utf8 --apply -' % (self.g2p_path, \
                                                                          escaped_word, self.lts_tool, self.lts_fname)

        pronun = subprocess.check_output(comm.encode('utf8'), shell=True, stderr=subprocess.STDOUT)

        ## remove the 'stack usage' output line -- its position varies:
        pronun = unicodedata.normalize('NFKD', pronun.decode('utf-8'))
        pronun = pronun.strip(' \n').split('\n')

        assert len(pronun) >= 2, str(pronun)  ## ==   -->   >=     to handle extra warnings

        normalised_word = unicodedata.normalize('NFKD', word)
        for line in pronun:
            if 'stack usage' not in line and normalised_word in line:
                pronun = line

        (outword, pronun) = re.split('\s+', pronun, maxsplit=1)
        outword = unicodedata.normalize('NFKD', outword)
        word = unicodedata.normalize('NFKD', word)

        if outword != word:
            print(outword + ' as outword does not match ' + word)

        return pronun


def main():

    experiment = G2P_Experiment()

    # if training:
    #print('train model ...')
    #experiment.train_sequitur_g2p()

    # if testing:
    in_file = open('data/g2p_dev_87.txt')
    test_data = in_file.readlines()
    errors = []
    for line in test_data:
        word, transcr = line.split('\t')

        pron = experiment.get_oov_pronunciation(word)
        if pron != transcr.strip():
            errors.append(word + '\tg2p: ' + pron + '\ttest: ' + transcr.strip())

    print('Errors: ' + str(len(errors)))
    print('Error rate: ' + str((len(errors)/len(test_data)) * 100.0) + '%')

    with open('g2p_test_results_87_clean.txt', 'w') as f:
        f.write('Errors: ' + str(len(errors)) + '\n')
        f.write('Error rate: ' + str((len(errors) / len(test_data)) * 100.0) + '%\n')
        for entry in errors:
            f.write(entry + '\n')


if __name__ == '__main__':

    main()
