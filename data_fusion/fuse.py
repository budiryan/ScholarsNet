#!/usr/bin/python3

import json
import sqlite3
import numpy as np

path = '../sqlite/paperDB.db'
connection = sqlite3.connect(path)
cursor = connection.cursor()

def fetch(cursor, index):
    return cursor.execute('select * from papers limit 1 offset ' + str(index)).fetchone()

def remove(cursor, index):
    cursor.execute('delete from papers limit 1 offset ' + str(index))

def insert(cursor, entry):
    cursor.execute('insert into papers values(?,?,?,?,?,?,?,?,?)', entry)

with open('jaccard_sed2.json', 'r') as f:
    data = json.load(f)

visited = []

for entry in data:

    i = entry['i']
    if i in visited:
        continue
        
    visited.append(i)

    old_record = [fetch(cursor, entry['i'])]
    old_length = [[len(str(x)) for x in old_record[-1]]]
    remove(cursor, entry['i'])
    for pair in data:
        if pair['i'] == i:
            old_record.append(fetch(cursor, pair['j']))
            old_length.append([len(str(x)) for x in old_record[-1]])
            remove(cursor, pair['j'])
 
    max_attr = np.argmax(old_length, axis = 0)

    new_record = []
    for r in range(len(old_record[0])):
        new_record.append(old_record[max_attr[r]][r])

    insert(cursor, new_record)

connection.commit()
