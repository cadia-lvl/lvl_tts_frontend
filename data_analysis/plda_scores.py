#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Compute averages of PLDA scores:

- of each speaker to all his/her utterances
- of each speaker to all other utterances
- of each speaker to each speaker (speaker by speaker)

Takes a trials_out file from Kaldi plda-scores computation as input:

speaker_id  utt_id  plda_score

"""
import sys


in_file = sys.argv[1]
out_dir = sys.argv[2]


def add_to_dict(speaker_dict, speaker, score):
    if speaker in speaker_dict:
        speaker_dict[speaker].append(float(score))
    else:
        speaker_dict[speaker] = [float(score)]


# keeps the scores of a speaker against all other speakers
speaker2all = {}
# keeps the socres of a speaker against his own utterances
speaker2self = {}
# keeps the scores of all pairs of speakers
speakerByspeaker = {}

for line in open(in_file).readlines():
    speaker, utt_id, score = line.split()
    # utt_id formats: ban_00737_00006753614, ism_1140_6520960459
    ref_speaker = utt_id[utt_id.index('_') + 1:utt_id.index('_', 5)]
    # google is specific, check if analysing other datasets
    if speaker == '1669' or ref_speaker == '1669':
        continue
    if speaker == ref_speaker:
        add_to_dict(speaker2self, speaker, score)

    else:
        add_to_dict(speaker2all, speaker, score)
        add_to_dict(speakerByspeaker, speaker + '_' + ref_speaker, score)


def create_avg_dict(speaker_dict):
    avg_dict = {}
    sum_avg = 0
    for spk in speaker_dict.keys():
        scores = speaker_dict[spk]
        sum_scores = sum(scores)
        avg = sum_scores/float(len(scores))
        avg_dict[spk] = avg
        sum_avg += avg

    return avg_dict, sum_avg


def write_dict(filename, dict2write):
    out = open(filename, 'w')
    for it in dict2write.keys():
        out.write(it + '\t' + str(dict2write[it]))
        out.write('\n')
    out.close()


res_speaker2self, speaker2self_avg = create_avg_dict(speaker2self)
res_speaker2all, speaker2all_avg = create_avg_dict(speaker2all)
res_speakerByspeaker, speakerByspeaker_avg = create_avg_dict(speakerByspeaker)

write_dict(out_dir + '/speaker2self.txt', res_speaker2self)
write_dict(out_dir + '/speaker2all.txt', res_speaker2all)
write_dict(out_dir + '/speakerByspeaker.txt', res_speakerByspeaker)

print('avg speaker2self: ' + str(speaker2self_avg/len(speaker2self)))
print('avg speaker2all: ' + str(speaker2all_avg/len(speaker2all)))
print('avg speakerByspeaker: ' + str(speakerByspeaker_avg/len(speakerByspeaker)))

