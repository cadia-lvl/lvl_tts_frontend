#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Compare two dictionary files and write out a new dictionary where items contained in dictionary2 are filtered
out of dictionary1.

Write out a new dictionary.

input format:

word    t r a n s c r i p t i o n
...



"""

import sys

frob_file1 = sys.argv[1]
frob_file2 = sys.argv[2]

main_lexicon = []

for line in open(frob_file1).readlines():
    #word, transcr = line.strip().split('\t')
    main_lexicon.append(line.strip())

to_remove = []

for line in open(frob_file2):
    #word, transcr = line.strip().split('\t')
    to_remove.append(line.strip())

print(str(len(to_remove)))
new_lexicon = []

for item in main_lexicon:
    if item not in to_remove:
        new_lexicon.append(item)

#new_lexicon = [x for x in main_lexicon if x not in to_remove]

#found = [x for x in main_lexicon if x in to_remove]

print('new: ' + str(len(new_lexicon)))
#print('remove: ' + str(len(found)))

with open(frob_file1 + '_filtered.txt', 'w') as f:
    for item in new_lexicon:
        f.write(item + '\n')
