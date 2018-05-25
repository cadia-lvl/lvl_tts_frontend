#!/usr/bin/env python3

"""
Ensure that the input transcripts only contain valid symbols.
For each non-valid symbol:
- check if a correction is available
- if yes, correct and report
- if not, report the error


General rules:
1) orhtographical letter instead of API symbol:
'e' should be replaced by 'ɛ', if it is not followed by 'i' ('ei' is valid)
'b' should be replaced by 'p'
'y' should be replaced by 'ʏ' if it is not preceded by 'œ' ('œy' is valid)
'o' should be replaced by 'ɔ' if it is not followed by 'u' ('ou' is valid)
'ö' should be replaced by 'œ'

2) wrongly placed diacritics
'ŋ̥' should be replaced by 'ŋ̊ '
'k̥' should be replaced by 'k'
'p̥' should be replaced by 'p'

3) non-allowed length marks
check 'yi:' transcriptions (ugi_variations.txt)
check 'ɔiː' transcriptions (ogi_variations.txt)
'pː' should be replaced by 'p'
'nː' should be replaced by 'n'
'lː' should be replaced by 'l'
'tː' should be replaced by 't'
'jː' should be replaced by 'j'
'ɣː' should be replaced by 'ɣ'
'vː' should be replaced by 'v'
'sː' should be replaced by 's'
'ːː' should be replaced by 'ː'
'mː' should be replaced by 'm'
'ðː' should be replaced by 'ð'

4) Uppercase letters
'A' should be replaced by 'a'
'U' should be replaced by 'ʏ'
'S' should be replaced by 's'
'V' should be replaced by 'v'
'L' should be replaced by 'l'

5) Superfluous symbols
remove '/'
remove '\'

6) Word separation symbols
Collect entries containing '#', ' ', or '-'

7) Not clear errors

Collect entries containing '0', '_'

"""

import sys


non_valid_symbols = {'b': 'p',
                    'ö': 'œ',
                    '\u014b\u0325': '\u014b\u030a',  #'ŋ̥': 'ŋ̊ ',
                    'k̥': 'k',
                    'p̥': 'p',
                    'pː': 'p',
                    'nː': 'n',
                    'lː': 'l',
                    'tː': 't',
                    'jː': 'j',
                    'ɣː': 'ɣ',
                    'vː': 'v',
                    'sː': 's',
                    'ːː': 'ː',
                    'mː': 'm',
                    'ðː': 'ð',
                    'A': 'a',
                    'U': 'ʏ',
                    'S': 's',
                    'V': 'v',
                    'L': 'l'
                     }

diphthongs_w_length = {'ʏiːjɪ': 'ʏijɪ',
                     'ɔiːjɪ': 'ɔijɪ'}

context_dependent_symbols = {'e': ('ɛ', 'ei'),
                            'y': ('ʏ', 'œy'),
                            'o': ('ɔ', 'ou')}

symbols_to_remove = ['\\', '/', '//', '///']

separation_symbols = ['#', '-', ' ']

unknown_errors = ['0', '_']

max_phone_len = 3

corrected_context_dep = []
corrected = []
unknown = []

dict_out = []

UNKNOWN = 'UNKNOWN'


def validate_phonemes(phone_str):
    if phone_str in non_valid_symbols:
        return non_valid_symbols[phone_str], len(phone_str)
    if phone_str in symbols_to_remove:
        return '', len(phone_str)
    if phone_str in separation_symbols:
        return UNKNOWN, len(UNKNOWN)
    if phone_str in unknown_errors:
        return UNKNOWN, len(UNKNOWN)

    return phone_str, len(phone_str)


def context_dependent_error(phone_str):
    diph_1 = ''
    diph_2 = ''
    for i in range(0,len(phone_str)):
        c = phone_str[i]
        if c in context_dependent_symbols:
            tup = context_dependent_symbols[c]
            if i > 0:
                diph_1 = phone_str[i-1] + c
            if i < len(phone_str) - 1:
                diph_2 = c + phone_str[i+1]

            if diph_1 == tup[1] or diph_2 == tup[1]:
                continue

            else:
                correction = phone_str[:i] + tup[0] + phone_str[i+1:]
                corrected_context_dep.append(phone_str + '\t' + correction)
                return correction

    return phone_str


def correct_diphthongs(phone_string):
    for elem in diphthongs_w_length.keys():
        phone_string = phone_string.replace(elem, diphthongs_w_length[elem])

    return phone_string


def correct_transcript(phone_string):
    offset = 0
    l = max_phone_len
    phone_len = len(phone_string)
    while offset < len(phone_string):
        repl_len = 0
        while l > 0:
            repl, repl_len = validate_phonemes(phone_string[offset: offset + l])
            if repl == UNKNOWN:
                unknown.append(phone_string)
                return phone_string, repl
            elif repl != phone_string[offset: offset + l]:
                phone_string = phone_string[: offset] + repl + phone_string[offset + repl_len:]
                if repl_len > 1:
                    offset += repl_len - 1
                break
            l -= 1

        offset += 1
        l = max_phone_len

    return phone_string, repl


def write_list(filename, list2write):

    with open(filename, 'w') as f:
        for item in list2write:
            f.write(item + '\n')


def main():
    frob_file = sys.argv[1]

    for line in open(frob_file).readlines():
        word, transcr = line.split('\t')

        corr_transcr = context_dependent_error(transcr.strip())
        corr_transcr = correct_diphthongs(corr_transcr)

        corr_transcr, repl = correct_transcript(corr_transcr)

        if repl == UNKNOWN:
            #print(line.strip())
            continue

        elif corr_transcr != transcr.strip():
            corrected.append(transcr.strip() + '\t' + corr_transcr)
            dict_out.append(word + '\t' + corr_transcr)

        else:
            dict_out.append(line.strip())

    write_list('context_dep_errors_2.txt', corrected_context_dep)
    write_list('replaced_errors_2.txt', corrected)
    write_list('unknown_2.txt', unknown)
    write_list(frob_file + '_consistent.txt', dict_out)


if __name__ == '__main__':
    main()

