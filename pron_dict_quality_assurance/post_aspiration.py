#!/usr/bin/env python3

# Ensures that plosives in the beginning of a word, followed by a vowel or a liquid (r)
# are transcribed with post aspiration (/pʰtʰkʰ/).
# Input file format: <word>\t<ipa-transcript>[further columns not considered]

import sys, csv, re


def main():
    import argparse
    parser = argparse.ArgumentParser(description='post aspiration',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', type=argparse.FileType('r'), default=sys.stdin,
                        help='Input file')
    parser.add_argument('-o', '--output', type=argparse.FileType('w'), default=sys.stdout,
                        help='Output file')

    args = parser.parse_args()

    for line in args.input:
        line_list = line.split('\t')
        if re.match('[pP][aeiouyáéíóúýöæjrv].*', line):
            if not re.match('pʰ.+', line_list[1]):
                new_ipa = line_list[1].replace('p', 'pʰ', 1)
                line_list[1] = new_ipa
        if re.match('[tT][aeiouyáéíóúýöæjrv].*', line):
            if not re.match('tʰ.+', line_list[1]):
                new_ipa = line_list[1].replace('t', 'tʰ', 1)
                line_list[1] = new_ipa
        if re.match('[kK][aouáóúörv].*', line):
            if not re.match('kʰ.+', line_list[1]):
                new_ipa = line_list[1].replace('k', 'kʰ', 1)
                line_list[1] = new_ipa
        if re.match('[kK][eiéíyýæj].*', line):
            if not re.match('cʰ.+', line_list[1]):
                new_ipa = line_list[1].replace('c', 'cʰ', 1)
                line_list[1] = new_ipa

        print(('\t').join(line_list).strip())


if __name__ == '__main__':
    main()
