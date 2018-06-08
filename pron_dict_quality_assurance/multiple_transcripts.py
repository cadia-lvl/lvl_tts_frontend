#!/usr/bin/env python3

"""

Filters words having multiple transcriptions and writes to file. Also keeps track
on unique words belonging to this file and writes to another file.
Takes a pronunciation dictionary as an input.

"""
import sys
import re

KEEP_BOTH = 'KEEP_BOTH'
NO_CHOICE = 'NO_CHOICE'


def choose_transcript(result_arr, transcr1, transcr2, word):

    if transcr1 == transcr2:
        return transcr1

    if ('k', 'x') in result_arr:
        return transcr1
    if ('x', 'k') in result_arr:
        return transcr2
    if ('n̥', 'n') in result_arr or ('ŋ̊', 'ŋ') in result_arr or ('ɲ̊', 'ɲ') in result_arr or ('m̥', 'm') in result_arr or ('r̥', 'r') in result_arr:
        return transcr1
    if ('n','n̥') in result_arr or ('ŋ', 'ŋ̊') in result_arr or ('ɲ', 'ɲ̊') in result_arr or ('m', 'm̥') in result_arr or ('r', 'r̥') in result_arr:
        return transcr2
    if ('l̥', 'l') in result_arr or ('t', '') in result_arr:
        if re.match('.+ll[aáeéiíoóuúyýöæ].*', word):
            return KEEP_BOTH
        else:
            return transcr1
    if ('l', 'l̥') in result_arr or ('', 't') in result_arr:
        if re.match('.+ll[aáeéiíoóuúyýöæ].*', word):
            return KEEP_BOTH
        else:
            return transcr2
    if ('c', 'k') in result_arr or ('h k', 'x') in result_arr or ('', 'k') in result_arr:
        return transcr1
    if ('k', 'c') in result_arr or ('x', 'h k') in result_arr or ('k', '') in result_arr:
        return transcr2

    else:
        return NO_CHOICE


def compare_same_len(transcr_arr1, transcr_arr2):
    result = []
    for i in range(len(transcr_arr1)):
        if transcr_arr1[i] != transcr_arr2[i]:
            result.append((transcr_arr1[i], transcr_arr2[i]))

    return result


def init_match_matrix(arr1, arr2):
    """
    Initializes a len(arr1) x len(arr2) matrix and set each matching cell to 'True'
    :param arr1:
    :param arr2:
    :return:
    """
    # create a arr1 x arr2 matrix
    match_matrix = [None] * len(arr1)
    for i in range(len(arr1)):
        match_matrix[i] = [None] * len(arr2)

    end_1 = len(arr1)
    end_2 = len(arr2)
    # set matching cells to 'True'
    for i in range(len(arr2)):
        if i > end_1 or i > end_2:
            # already checked all indices upto index i from the end
            break
        if arr1[i] == arr2[i]:
            match_matrix[i][i] = True

        else:
            # check matches from end
            while end_1 > i and end_2 > i:
                end_1 -= 1
                end_2 -= 1
                if arr1[end_1] == arr2[end_2]:
                    match_matrix[end_1][end_2] = True
                else:
                    break

            # find matches with uneven indices, arr2[i] is the anchor, we search for matches in arr1
            for j in range(i, end_1):
                if arr2[i] == arr1[j]:
                    match_matrix[j][i] = True
                    break

    return match_matrix


def compare_transcripts(transcr1, transcr2):
    """
    Compare two transcripts and extract substitutions and/or insertions.
    Example:
    transcr1: r eiː k j a v iː k ʏ r v eiː j ɪ
    transcr2: r eiː c a v i k ʏ r v ei j ɪ

    returns a list of tuples containing non-matching phones: [('k j', 'c'), ('iː', 'i'), ('eiː', 'ei')]

    Could easily be extended to collect the corresponding indices, but no need for that by now.

    :param transcr1:
    :param transcr2:
    :return: a list of tuples of non-matching phones
    """

    arr1 = transcr1.split()
    arr2 = transcr2.split()
    result = []

    if len(arr1) == len(arr2):
        return compare_same_len(arr1, arr2)

    if len(arr1) < len(arr2):
        return compare_transcripts(transcr2, transcr1)

    match_matrix = init_match_matrix(arr1, arr2)

    # create a list of tuples with cell coordinates of all 'True' cells
    matches = [(index, row.index(True)) for index, row in enumerate(match_matrix) if True in row]

    # find all non-matching cells and collect inserts and substitutions
    last_tup_1 = -1
    last_tup_2 = -1
    for i in range(len(matches)):
        tup = matches[i]
        # no gap, hence no substitution/insertion before the current match
        # e.g.: (0,0), (1,1) etc., or (5,4), (6,5), etc.
        if tup[0] == last_tup_1 + 1 and tup[1] == last_tup_2 + 1:
            last_tup_1 = tup[0]
            last_tup_2 = tup[1]
        else:
            sub1 = []
            sub2 = []
            # collect the phones from the gap
            for j in range(last_tup_1 + 1, tup[0]):
                sub1.append(arr1[j])
            for j in range(last_tup_2 + 1, tup[1]):
                sub2.append(arr2[j])

            sub_tup = (' '.join(sub1), ' '.join(sub2))

            result.append(sub_tup)
            last_tup_1 = tup[0]
            last_tup_2 = tup[1]
            if sub_tup == ('', ''):
                print(' '.join(arr1) + ' -- ' + ' '.join(arr2))

    # insertion at the end of arr1?
    if len(arr1) > last_tup_1 + 1:
        ins = arr1[last_tup_1 + 1:]
        ins_tup = (' '.join(ins), '')
        print(' '.join(arr1) + ' -- ' + ' '.join(arr2))
        result.append(ins_tup)

    return result


def transcript_diff(entry_arr):
    """
    Find the differences in transcripts of the same word.
    :param entry_arr: array of entries 'word\tt r a n s c r i p t'
    :return: array of tuples [(diff1a, diff2a, ...), (diff1b, diff2b, ...)]
    """

    same_word = set()
    transcripts = []
    for entry in entry_arr:
        word, transcr = entry.split('\t')
        same_word.add(word)
        if len(same_word) > 1:
            raise ValueError("not all words in the input are the same! " + str(same_word))

        transcripts.append(transcr)

    result = []
    if len(transcripts) == 2:
        result = compare_transcripts(transcripts[0], transcripts[1])
        chosen_transcript = choose_transcript(result, transcripts[0], transcripts[1], word)

    elif len(transcripts) > 2:
        reference_transcr = transcripts[0]
        for i in range(1,len(transcripts)):
            result.extend(compare_transcripts(reference_transcr, transcripts[i]))
            chosen_transcript = choose_transcript(result, reference_transcr, transcripts[i], word)

    else:
        raise ValueError("No transcripts to compare! " + str(transcripts))

    return result, chosen_transcript


def main():
    transcr_file = sys.argv[1]
    filtered_dictionary = []
    no_choice_made = []
    words_outfile = 'words_with_multiple_transcripts.txt'
    multiple_transcripts_outfile = 'multiple_transcripts.csv'

    multiple_transcripts = []
    lines2write = []
    transcript_diffs_stats = {}
    words_with_multiple_transcr = set()
    saved_last = []
    last = ""
    last_line = ""
    last_single = ''
    for line in open(transcr_file).readlines():
        arr = line.split('\t')
        word = arr[0]
        if word == last:
            if len(multiple_transcripts) == 0:
                multiple_transcripts.append(last_line)
            multiple_transcripts.append(line)
            words_with_multiple_transcr.add(word)
            last_single = ""
        elif len(multiple_transcripts) > 0:
            lines2write.extend(multiple_transcripts)
            transcr_diffs, chosen_transcript = transcript_diff(multiple_transcripts)
            if chosen_transcript == KEEP_BOTH:
                filtered_dictionary.extend(multiple_transcripts)
            elif chosen_transcript != NO_CHOICE:
                filtered_dictionary.append(last + '\t' + chosen_transcript)
            else:
                no_choice_made.extend(multiple_transcripts)
            for diff_tuple in transcr_diffs:
                if diff_tuple in transcript_diffs_stats:
                    val = transcript_diffs_stats[diff_tuple]
                    val.append(last)
                    transcript_diffs_stats[diff_tuple] = val
                elif diff_tuple[::-1] in transcript_diffs_stats:
                    # we don't care about the order in the tuple, ('k', 'c') equivalent to ('c', 'k')
                    val = transcript_diffs_stats[diff_tuple[::-1]]
                    val.append(last)
                    transcript_diffs_stats[diff_tuple[::-1]] = val

                else:
                    transcript_diffs_stats[diff_tuple] = [last]

            multiple_transcripts = []

        else:
            # a single entry or the first of more entries
            if last_single != '':
                filtered_dictionary.append(last_single)
            last_single = line

        last = word
        last_line = line

    print("Number of words with multiple transcripts: " + str(len(words_with_multiple_transcr)))

    out = open(words_outfile, 'w')
    for w in words_with_multiple_transcr:
        out.write(w + '\n')

    out = open(multiple_transcripts_outfile, 'w')
    out.writelines(lines2write)

    out = open('dict_step_5.txt', 'w')
    out.writelines(filtered_dictionary)

    out = open('no_choice.txt', 'w')
    out.writelines(no_choice_made)

    out = open('transcript_diff_stats.txt', 'w')
    for diff in sorted(transcript_diffs_stats, key=lambda x: len(transcript_diffs_stats[x]), reverse=True):
        out.write(str(diff) + '\t' + str(transcript_diffs_stats[diff]) + '\t' + str(len(transcript_diffs_stats[diff])) + '\n')

    out = open('transcript_stats_only.txt', 'w')
    for diff in sorted(transcript_diffs_stats, key=lambda x: len(transcript_diffs_stats[x]), reverse=True):
        out.write(
            str(diff) + '\t' + str(len(transcript_diffs_stats[diff])) + '\n')


if __name__ == '__main__':
    main()
