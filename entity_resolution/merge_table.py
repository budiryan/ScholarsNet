#!/usr/bin/env python

import sqlite3

table_names = ['arxiv', 'acm', 'dblp', 'ieee']

mapping = {'abstract' : ['abstract'      , 'abstract'     , 'abstracts'     , 'abstract'     ],
           'author'   : ['author'        , 'authors'      , 'author'        , 'author'       ],
           'title'    : ['title'         , 'title'        , 'title'         , 'title'        ],
           'url'      : ['link'          , 'pdf_link'     , 'url'           , 'pdf_link'     ],
           'date'     : ['publish_date'  , 'time_added'   , 'year'          , 'published_in' ],
           'coauthors': ['other_authors' , 'other_authors', 'other_authors' , 'other_authors'],
           'doi'      : ['doi'           , 'doi'          , 'doi'           , 'doi'          ]}

connection = sqlite3.connect('../sqlite/scholarDB.db')
merge_connection = sqlite3.connect('../sqlite/paperDB.db')

cursor = connection.cursor()
merge_cursor = merge_connection.cursor()

for i in range(4):

    print table_names[i]
    cursor.execute('select ' + mapping['title'    ][i] + ','
                             + mapping['doi'      ][i] + ','
                             + mapping['abstract' ][i] + ','
                             + mapping['author'   ][i] + ','
                             + mapping['url'      ][i] + ','
                             + mapping['date'     ][i] + ','
                             + mapping['coauthors'][i] + ' from ' + table_names[i])

    entries = cursor.fetchall()
    for entry in entries:
        try:
            merge_cursor.execute('insert into papers values(?,?,?,?,?,?,?,?)', list(entry) + [table_names[i]])
        except:
            print entry[0]

merge_connection.commit()

