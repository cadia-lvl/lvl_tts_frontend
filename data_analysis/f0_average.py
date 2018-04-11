"""
Computes average F0 per speaker according to input directory (f0 folder)

"""
import os

f0_folder = '/Users/anna/F0/'

speaker2f0 = {}

for filename in os.listdir(f0_folder):
    spk_id = filename[4:8]
    if spk_id in speaker2f0:
        f0_arr = speaker2f0[spk_id]
    else:
        f0_arr = []

    for line in open(f0_folder + filename).readlines():
        if line.strip() == '0':
            continue
        else:
            f0_arr.append(float(line.strip()))

    speaker2f0[spk_id] = f0_arr

avg_f0 = {}
for spk in speaker2f0.keys():
    f0_arr = speaker2f0[spk]
    f0_sum = sum(f0_arr)
    f0_avg = f0_sum/len(f0_arr)
    avg_f0[spk] = f0_avg

for spk in avg_f0.keys():
    print(spk + '\t' + str(avg_f0[spk]))

