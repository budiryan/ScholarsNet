#!/usr/bin/env python

import sqlite3
import re

path = '../sqlite/paperDB.db'
connection = sqlite3.connect(path)
cursor = connection.cursor()

cursor.execute('select title from papers')
entries = cursor.fetchall()

l = len(entries)

with open('strict_compare.txt', 'w') as f:
    for i in range(l):
        for j in range(i + 1, l):
            s1 = entries[i][0]
            s2 = entries[j][0]
            s1 = re.sub('[^\w\s]', '', '' if s1 is None else s1).lower()
            s2 = re.sub('[^\w\s]', '', '' if s2 is None else s2).lower()
            if s1 == s2:
                f.write(str(i) + str(j))
                f.write(entries[i][0])
                f.write(entries[j][0])
                f.write('\n')

