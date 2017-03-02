#!/usr/bin/python3.5

import os
import json
import sqlite3

path = '../data_retrieval/arxiv/data/json/'

connection = sqlite3.connect('scholarDB.db')
with connection:
    cursor = connection.cursor()

    for f in os.listdir(path):
        traffic = json.load(open(path + f))
        for t in traffic[0:300]:
            try:
                cursor.execute('insert into arxiv values(?,?,?,?,?,?,?)', [t['category'], t['link'], t['publish'], t['summary'], t['title'], t['author'], t['arxiv-id']])
            except sqlite3.Error as e:
                print(e)
