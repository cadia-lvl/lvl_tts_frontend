#!/usr/bin/env python3

# Checks google file 'suggestions.csv' against an lvl version of the pron dict


import sys

pron_dict_in = sys.argv[1]
google_in = sys.argv[2]

google_list = []
pron_dict = []

for line in open(google_in).readlines():
    arr = line.split(',')
    google_list.append(arr[1])

for line in open(pron_dict_in).readlines():
    word, transcr = line.split('\t')
    pron_dict.append(word)
   # if word in google_list:
   #     print(line.strip())

missing = [x for x in google_list if x not in pron_dict]

for item in missing:
    print(item)