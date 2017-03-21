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
                print(t['arxiv-id'])
                cursor.execute('insert into arxiv values(?,?,?,?,?,?,?,?,?)', 
                            [t['category'], 
                             t['doi'], 
                             t['link'],
                             t['other_authors'],
                             t['title'], 
                             t['arxiv-id'],
                             t['author'],
                             t['publish'], 
                             t['summary']])
            except sqlite3.Error as e:
                print(e)
