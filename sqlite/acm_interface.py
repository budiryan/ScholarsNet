import json
import sqlite3


with open('../data_retrieval/acm_journal.json') as data_file:
    data = json.load(data_file)

connection = sqlite3.connect('scholarDB.db')
with connection:
    cursor = connection.cursor()
    count = 0
    for row in data:
        journal_category = row['journal category']
        abstract = row['abstract']
        volume = row['volume']
        authors = ""
        for author in row['authors']:
            authors += author
            if author != row['authors'][-1]:
                authors += ','
        title = row['title']
        citation_count = row['citation count']
        journal_category_description = row['journal category_description']
        pdf_link = row['pdf link']
        download_count = row['download count']
        time_added = row['time added']
        cursor.execute('insert into acm values(?,?,?,?,?,?,?,?,?,?)', [journal_category, abstract, volume, authors, title, citation_count, journal_category_description, pdf_link, download_count, time_added])
