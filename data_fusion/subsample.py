#!/usr/bin/env python3.5

import sys
import json
import numpy as np

filename = sys.argv[1] if len(sys.argv) > 1 else None

subsample_size = 100
is_TP = []

if filename is not None:
    with open(filename, 'r') as f:
        entries = json.load(f)

    perm = np.random.permutation(len(entries))[:subsample_size]

    for i in range(subsample_size):
        print('Entry ' + str(i) + ': Row ' + str(perm[i]))
        print('i: ' + str(entries[perm[i]]['i']) + ' j: ' + str(entries[perm[i]]['j']))
        # print('Score: ' + str(entries[perm[i]]['score']) + '\n' if 'score' in entries[perm[i]] else '', end = '')
        print('Title 1: ' + entries[perm[i]]['title1'])
        print('Title 2:' + entries[perm[i]]['title2'])
        print('Are they really the same? [y/n] ', end = '')
        is_TP.append(input() == 'y')
        print('')

    TP = np.sum(is_TP)
    print('TR count: ' + str(TP))
    print('TPR: ' + str(float(TP) / subsample_size))

