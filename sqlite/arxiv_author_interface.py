#!/usr/bin/python3.5

import os
import json
import sqlite3

path = '../data_retrieval/arxiv_author/data/'

connection = sqlite3.connect('scholarDB.db')
with connection:
    cursor = connection.cursor()

    for f in os.listdir(path):
        print(f)
        traffic = json.load(open(path + f))
        for t in traffic:
            try:
                cursor.execute('insert into arxiv_author values(NULL,?,?,?,?,?,?,?,?)', 
                                                                [t['category'], 
                                                                 t['link'], 
                                            ', '.join(a for a in t['other_authors'] if a != t['lead_author']),
                                                                 t['lead_author'],
                                                                 t['arxiv-id'],
                                                                 t['title'], 
                                                                 t['publish'], 
                                                                 t['summary']])
            except sqlite3.Error as e:
                print(e)

    try:
        cursor.execute('delete from arxiv_author where rowid not in (select min(rowid) from arxiv_author group by arxiv_id, lead_author)')
    except sqlite3.Error as e:
        print(e)
