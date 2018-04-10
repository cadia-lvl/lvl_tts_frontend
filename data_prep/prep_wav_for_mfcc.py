"""

Create a file, wav.scp, of the following format for an input folder:

is_is-althingi1_01-2011-11-30T16:18:39.715490 sox - -c1 -esigned -r16000 -twav -  < /data/Almannaromur/audio/is_is-althingi1_01-2011-11-30T16:18:39.715490.wav |
is_is-althingi1_01-2011-11-30T16:20:40.413136 sox - -c1 -esigned -r16000 -twav -  < /data/Almannaromur/audio/is_is-althingi1_01-2011-11-30T16:20:40.413136.wav |
is_is-althingi1_01-2011-11-30T16:21:13.014208 sox - -c1 -esigned -r16000 -twav -  < /data/Almannaromur/audio/is_is-althingi1_01-2011-11-30T16:21:13.014208.wav |
is_is-althingi1_01-2011-11-30T16:22:11.188176 sox - -c1 -esigned -r16000 -twav -  < /data/Almannaromur/audio/is_is-althingi1_01-2011-11-30T16:22:11.188176.wav |

where the input folder corresponds to /data/Almannaromur/audio/ in the example above

"""

import sys
import os

wav_folder = sys.argv[1]
out_folder = sys.argv[2]

if not os.path.exists(out_folder):
    os.makedirs(out_folder)

samplerate = '48000'
wav_cmd = 'sox - -c1 -esigned -r' + samplerate + ' -twav - '

wavscp = open(out_folder + '/wav.scp', 'w')
utt2spk = open(out_folder + '/utt2spk', 'w')

for filename in os.listdir(wav_folder):
    utt_id = filename[:filename.index('.wav')]
    spkr = filename[:4]
    print >> wavscp, '{} {} < {}/{} | '.format(utt_id, wav_cmd, wav_folder, filename)
    print >> utt2spk, utt_id, spkr


