#!/usr/bin/env python

import sqlite3
import editdistance
import json

path = '../sqlite/paperDB.db'
connection = sqlite3.connect(path)
cursor = connection.cursor()

cursor.execute('select * from papers')
entries = cursor.fetchall()

sed = []
temp = []

l = len(entries)

count = 0
result_array = []
for i in range(l):
    for j in range(i + 1, l):
        if i != j:
            s1 = '' if entries[i][0] is None else entries[i][0]
            s2 = '' if entries[j][0] is None else entries[j][0]
            d = editdistance.eval(s1, s2)
            if d < len(s1) / 4:
                print(str(i) + s1 + '\n')
                print(str(j) + s2 + '\n')
                print('Edit distance:' + str(d) + '\n')
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
                        "score": d < len(s1) / 4,
                        "count": count
                    }
                )
                if count % 1 == 0:
                    with open('string_edit_distance.json', 'w') as f:
                        json.dump(result_array, f, indent=4)
