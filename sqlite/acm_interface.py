import json
import sqlite3


with open('../data_retrieval/acm/acm_paper_doi.json') as data_file:
    data = json.load(data_file)

connection = sqlite3.connect('scholarDB.db')
with connection:
    cursor = connection.cursor()
    count = 0
    for row in data:
        journal_category = row['journal category']
        abstract = row['abstract']
        volume = row['volume']
        main_author = row['author']
        authors = ""
        for author in row['other_authors']:
            authors += author
            if author != row['other_authors'][-1]:
                authors += ','
        title = row['title']
        citation_count = row['citation count']
        journal_category_description = row['journal category_description']
        pdf_link = row['pdf link']
        download_count = row['download count']
        time_added = row['time added']
        doi = row['doi']
        cursor.execute('insert into acm values(?,?,?,?,?,?,?,?,?,?,?,?)', [journal_category, abstract, volume, main_author, title, citation_count, journal_category_description, pdf_link, download_count, time_added, authors, doi])
