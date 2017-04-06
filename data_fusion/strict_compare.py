#!/usr/bin/env python

import sqlite3
import re

path = '../sqlite/paperDB.db'
connection = sqlite3.connect(path)
cursor = connection.cursor()

cursor.execute('select title from papers')
entries = cursor.fetchall()

l = len(entries)

count = 0

with open('strict_compare.txt', 'w') as f:
    for i in range(l):
        for j in range(i + 1, l):
            s1 = entries[i][0]
            s2 = entries[j][0]
            s1 = re.sub('[^\w\s]|_', '', '' if s1 is None else s1).lower().strip()
            s2 = re.sub('[^\w\s]|_', '', '' if s2 is None else s2).lower().strip()
            if s1 == s2:
                f.write(str(i) + ' ' + str(j) + '\n')
                print(str(i) + ' ' + str(j) + '\n')

                if entries[i][0] is None:
                    f.write('title1: null' + '\n')
                    print('title1: null' + '\n')
                else:
                    f.write('title1: ' + entries[i][0] + '\n')
                    print('title1: ' + entries[i][0] + '\n')

                if entries[j][0] is None:
                    f.write('title2: null' + '\n')
                    print('title2: null' + '\n')
                else:
                    f.write('title2: ' + entries[j][0] + '\n')
                    print('title2: ' + entries[j][0] + '\n')

                print('\n')
                count += 1

    f.write('Total: ' + str(count))
