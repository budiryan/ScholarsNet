import json
import sqlite3


with open('../data_retrieval/ieee_full_page.json') as data_file:
    data = json.load(data_file)

connection = sqlite3.connect('scholarDB.db')
with connection:
    cursor = connection.cursor()
    count = 0
    for row in data:
        authors = ""
        for author in row['authors']:
            authors += author
            if author != row['authors'][-1]:
                authors += ','
        cursor.execute('insert into ieee values(?,?,?,?,?,?,?,?)', [row['Electronic ISBN'], row['abstract'], row[
                       'Date of Conference'], row['Print on Demand ISBN'], row['published in'], row['title'], authors, row['PDF Link']])
