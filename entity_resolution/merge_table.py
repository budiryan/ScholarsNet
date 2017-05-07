#!/usr/bin/env python

import sqlite3

table_names = ['arxiv', 'acm', 'dblp', 'ieee']

mapping = {'abstract' : ['abstract'      , 'abstract'     , 'abstracts'     , 'abstract'     ],
           'author'   : ['author'        , 'authors'      , 'author'        , 'author'       ],
           'title'    : ['title'         , 'title'        , 'title'         , 'title'        ],
           'url'      : ['link'          , 'pdf_link'     , 'url'           , 'pdf_link'     ],
           'date'     : ['publish_date'  , 'time_added'   , 'year'          , 'time_of_conference' ],
           'coauthors': ['other_authors' , 'other_authors', 'other_authors' , 'other_authors'],
           'doi'      : ['doi'           , 'doi'          , 'doi'           , 'doi'          ]}

connection = sqlite3.connect('../sqlite/scholarDB.db')
merge_connection = sqlite3.connect('../sqlite/paperDB.db')

cursor = connection.cursor()
merge_cursor = merge_connection.cursor()
doi_list = []
title_list = []

for i in range(4):
    print('Now adding: ', table_names[i])
    cursor.execute('select ' + mapping['title'    ][i] + ','
                             + mapping['doi'      ][i] + ','
                             + mapping['abstract' ][i] + ','
                             + mapping['author'   ][i] + ','
                             + mapping['url'      ][i] + ','
                             + mapping['date'     ][i] + ','
                             + mapping['coauthors'][i] + ','
                             + ' rowid' + ' from ' + table_names[i])

    entries = cursor.fetchall()
    for entry in entries:
        try:
            if (entry[0] not in title_list) and (entry[1] not in doi_list):
                merge_cursor.execute('insert into papers values(?,?,?,?,?,?,?,?,?)', list(entry) + [table_names[i]])
                title_list.append(entry[0])
                doi_list.append(entry[1])
        except:
            print(entry[0])

merge_connection.commit()
