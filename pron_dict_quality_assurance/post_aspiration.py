#!/usr/bin/env python3

# Ensures that plosives in the beginning of a word, followed by a vowel or a liquid (r)
# are transcribed with post aspiration (/pʰtʰkʰ/).
# Input file format: <word>\t<ipa-transcript>[further columns not considered]

import sys, csv, re


def write_list(filename, list2write):

    with open(filename, 'w') as f:
        for line in list2write:
            f.write(line)


def find_postaspir(input_file):

    c_postaspir = []
    k_postaspir = []
    p_postaspir = []
    t_postaspir = []

    for line in input_file:
        word, transcr = line.strip().split('\t')
        if re.search('cʰ', transcr):
            c_postaspir.append(line)
        if re.search('kʰ', transcr):
            k_postaspir.append(line)
        if re.search('pʰ', transcr):
            p_postaspir.append(line)
        if re.search('tʰ', transcr):
            t_postaspir.append(line)

    write_list('c_postaspir.txt', c_postaspir)
    write_list('k_postaspir.txt', k_postaspir)
    write_list('p_postaspir.txt', p_postaspir)
    write_list('t_postaspir.txt', t_postaspir)


def find_beginning_postaspir(input_file):
    c_postaspir = []
    k_postaspir = []
    p_postaspir = []
    t_postaspir = []

    for line in input_file:
        word, transcr = line.strip().split('\t')
        if re.match('cʰ.+', transcr):
            c_postaspir.append(line)
        if re.match('kʰ.+', transcr):
            k_postaspir.append(line)
        if re.match('pʰ.+', transcr):
            p_postaspir.append(line)
        if re.match('tʰ.+', transcr):
            t_postaspir.append(line)

    write_list('c_beginningpostaspir.txt', c_postaspir)
    write_list('k_beginningpostaspir.txt', k_postaspir)
    write_list('p_beginningpostaspir.txt', p_postaspir)
    write_list('t_beginningpostaspir.txt', t_postaspir)



def find_missing_postaspir(input_file):
    c_postaspir = []
    k_postaspir = []
    p_postaspir = []
    t_postaspir = []

    for line in input_file:
        word, transcr = line.split('\t')
        if re.match('[pP][aeiouyáéíóúýöæjlrv].*', word):
            if not re.match('pʰ.+', transcr):
                p_postaspir.append(line)
        if re.match('[tT][aeiouyáéíóúýöæjrv].*', word):
            if not re.match('tʰ.+', transcr):
                t_postaspir.append(line)
        if re.match('[kK][aouáóúölrv].*', word):
            if not re.match('kʰ.+', transcr):
                k_postaspir.append(line)
        if re.match('[hH]v[aeiouyáéíóúýöæjr].*', word):
            if not re.match('kʰ.+', transcr):
                k_postaspir.append(line)
        if re.match('[kK][eiéíyýæj].*', word):
            if not re.match('cʰ.+', transcr):
                c_postaspir.append(line)

    write_list('c_missingpostaspir.txt', c_postaspir)
    write_list('k_missingpostaspir.txt', k_postaspir)
    write_list('p_missingpostaspir.txt', p_postaspir)
    write_list('t_missingpostaspir.txt', t_postaspir)


def ensure_postaspir(input_file):
    for line in input_file:
        word, transcr = line.split('\t')
        if re.match('[pP][aeiouyáéíóúýöæjlrv].*', word):
            if not re.match('pʰ.+', transcr):
                new_ipa = transcr.replace('p', 'pʰ', 1)
                transcr = new_ipa
        if re.match('[tT][aeiouyáéíóúýöæjrv].*', word):
            if not re.match('tʰ.+', transcr):
                new_ipa = transcr.replace('t', 'tʰ', 1)
                transcr = new_ipa
        if re.match('[kK][aouáóúölrv].*', word):
            if not re.match('kʰ.+', transcr):
                new_ipa = transcr.replace('k', 'kʰ', 1)
                transcr = new_ipa
        if re.match('[hH]v[aeiouyáéíóúýöæ].*', word):
            if not re.match('kʰ.+', transcr):
                new_ipa = transcr.replace('k', 'kʰ', 1)
                transcr = new_ipa
        if re.match('[kK][eiéíyýæj].*', word):
            if not re.match('cʰ.+', transcr):
                new_ipa = transcr.replace('c', 'cʰ', 1)
                transcr = new_ipa

        print(word + '\t' + transcr.strip())


def main():
    import argparse
    parser = argparse.ArgumentParser(description='post aspiration',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', type=argparse.FileType('r'), default=sys.stdin,
                        help='Input file')
    parser.add_argument('-o', '--output', type=argparse.FileType('w'), default=sys.stdout,
                        help='Output file')

    args = parser.parse_args()

    #find_postaspir(args.input)
    #find_missing_postaspir(args.input)
    #find_beginning_postaspir(args.input)
    ensure_postaspir(args.input)


if __name__ == '__main__':
    main()
