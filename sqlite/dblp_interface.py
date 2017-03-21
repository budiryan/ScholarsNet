#!/usr/bin/python3.5

import os
import xml.etree.ElementTree as ET
import sqlite3

path = '../../dblp.xml'

connection = sqlite3.connect('scholarDB.db')
with connection:
    cursor = connection.cursor()

    print('Parsing xml')
    tree = ET.parse(path)
    root = tree.getroot()

    print('Inserting to table')
    for child in root[0:10000]:
        try:
            author = ''
            title = ''
            pages = ''
            year = ''
            volume = ''
            journal = ''
            number = ''
            url = ''
            doi = ''
            summary = ''
            for c in child:
                if c.tag == 'author':
                    author += c.text + ', '
                elif c.tag == 'title':
                    title = c.text
                elif c.tag == 'pages':
                    pages = c.text
                elif c.tag == 'year':
                    year = c.text
                elif c.tag == 'volume':
                    volume = c.text
                elif c.tag == 'journal':
                    journal = c.text
                elif c.tag == 'number':
                    number = c.text
                elif c.tag == 'url':
                    url = 'http://dblp.uni-trier.de/' + c.text
                elif c.tag == 'ee':
                    splits = c.text.split('.org/', 1)
                    doi = splits[1] if len(splits) == 2 else ''
                elif c.tag == 'summary':
                    summary = c.text
                
            cursor.execute('insert into dblp values(?,?,?,?,?,?,?,?,?,?)', [author, title, pages, year, volume, journal, number, doi, url, summary])

        except sqlite3.Error as e:
            print(e)
