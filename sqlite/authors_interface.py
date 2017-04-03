import json
import sqlite3


with open('../data_retrieval/authors/author_info.json') as data_file:
    data = json.load(data_file)

connection = sqlite3.connect('scholarDB.db')
with connection:
    cursor = connection.cursor()
    for row in data:
        name = row['name']
        website = row['website']
        email = row['email']
        photo = row['photo']
        affiliations = ''
        for a in row['university']:
            affiliations += a
            if a != row['university'][-1]:
                affiliations += '|'
        citation_count = row['citation count']
        publication_count = row['publication count']
        publication_years = row['publication years']
        total_downloads = row['total downloads']
        cursor.execute('insert into authors values(?,?,?,?,?,?,?,?,?)', [name, website, email, photo, affiliations, citation_count, publication_count, publication_years, total_downloads])
