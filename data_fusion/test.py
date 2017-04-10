#!/usr/bin/env python3.5

import sqlite3
import re

rv = sqlite3.connect('../sqlite/paperDB.db')
cursor = rv.cursor()

def get_author_papers(name):
    cursor.execute('select * from papers')
    rows = cursor.fetchall()

    all_authors = []

    for row in rows:
        authors = [row[3]]
        authors += row[6].split(', ')

        for i in range(len(authors)):
            if authors[i] != None and authors[i] != '':
                authors[i] = re.sub('\(.*\)', '', authors[i])

        abbr_authors = []
        for name in authors:
            if name == None or name == '':
                continue

            full_name = ''
            names = name.split(' ')
            for n in names[:-1]:
                if n != None and n != '':
                    full_name += n[0] + ' '
            full_name += names[-1]
            abbr_authors.append(full_name)

        all_authors.append(abbr_authors)

    papers = []

    for i in range(len(rows)):
        print(all_authors[i])
        if name in all_authors[i]:
            papers.append(rows[i][0])

    return papers

get_author_papers('j')
