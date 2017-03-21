import json
import sqlite3


with open('../data_retrieval/ieee/ieee_doi.json') as data_file:
    data = json.load(data_file)

connection = sqlite3.connect('scholarDB.db')
with connection:
    cursor = connection.cursor()
    count = 0
    for row in data:
        if row['doi'] is None:
            continue
        other_authors = ""
        main_author = row['authors']
        for author in row['other authors']:
            other_authors += author
            if author != row['other authors'][-1]:
                other_authors += ','
        cursor.execute('insert into ieee values(?,?,?,?,?,?,?,?,?,?)', [row['Electronic ISBN'], row['abstract'], row[
                       'Date of Conference'], row['Print on Demand ISBN'], row['published in'], row['title'], main_author, row['PDF Link'], other_authors, row['doi']])
