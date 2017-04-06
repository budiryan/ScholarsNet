#!/usr/bin/env python

import sqlite3
import re
import json

path = '../sqlite/paperDB.db'
connection = sqlite3.connect(path)
cursor = connection.cursor()

cursor.execute('select * from papers')
entries = cursor.fetchall()

l = len(entries)

count = 0
result_array = []
for i in range(l):
    for j in range(i + 1, l):
        s1 = entries[i][0]
        s2 = entries[j][0]
        s1 = re.sub('[^\w\s]|_', '', '' if s1 is None else s1).lower().strip()
        s2 = re.sub('[^\w\s]|_', '', '' if s2 is None else s2).lower().strip()
        if s1 == s2:
            print(str(i) + ' ' + str(j) + '\n')

            if entries[i][0] is None:
                print('title1: null' + '\n')
            else:
                print('title1: ' + entries[i][0] + '\n')

            if entries[j][0] is None:
                print('title2: null' + '\n')
            else:
                print('title2: ' + entries[j][0] + '\n')

            print('\n')
            count += 1
            result_array.append(
                {
                    "i": i,
                    "title1": entries[i][0],
                    "url1": entries[i][4],
                    "j": j,
                    "title2": entries[j][0],
                    "url2": entries[j][4],
                    "count": count
                }
            )
            if count % 1 == 0:
                with open('strict_compare.json', 'w') as f:
                    json.dump(result_array, f, indent=4)

f.write('Total: ' + str(count))
