#!/usr/bin/env python

import sqlite3
import editdistance
import numpy.random as nr

path = '../sqlite/paperDB.db'
connection = sqlite3.connect(path)
cursor = connection.cursor()

cursor.execute('select title from papers')
entries = cursor.fetchall()

sed = []
temp = []

l = len(entries)

count = 0

with open('string_edit.txt', 'w') as f:
    for i in range(l):
        for j in range(i + 1, l):
            if i != j:
                s1 = '' if entries[i][0] is None else entries[i][0]
                s2 = '' if entries[j][0] is None else entries[j][0]
                d = editdistance.eval(s1, s2) 
                if d < len(s1) / 4:
                    f.write(str(i) + s1 + '\n')
                    print(str(i) + s1 + '\n')
                    f.write(str(j) + s2 + '\n')
                    print(str(j) + s2 + '\n')
                    f.write('Edit distance:' +  str(d) + '\n')
                    print('Edit distance:' +  str(d) + '\n')
                    f.write('\n\n')
                    print('\n')
                    count += 1

    f.write('Total: ' + str(count))
