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

with open('string_edit.txt', 'w') as f:
    for i in range(l):
        for j in range(i + 1, l):
            if i != j:
                s1 = '' if entries[i][0] is None else entries[i][0]
                s2 = '' if entries[j][0] is None else entries[j][0]
                a = editdistance.eval(s1, s2) 
                if a < len(s1) / 3:
                    f.write(str(i) + s1)
                    f.write(str(j) + s2)
                    f.write('Edit distance:' +  a)
                    f.write('\n')
