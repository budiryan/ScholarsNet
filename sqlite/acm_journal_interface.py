import json
import sqlite3


with open('../data_retrieval/acm/acm_journal_information.json') as data_file:
    data = json.load(data_file)

connection = sqlite3.connect('scholarDB.db')
with connection:
    cursor = connection.cursor()
    for row in data:
        cursor.execute('insert into acm_journals values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                       [row['journal category'], row['journal category_description'], row['citation count'], row['total downloads'],
                        row['publication count'], row['available for download'], row['publication years'], row['first most downloaded article'], row['second most downloaded article'], row['third most downloaded article'], row['fourth most downloaded article'], row['fifth most downloaded article'], row['sixth most downloaded article'], row['seventh most downloaded article'], row['eight most downloaded article'], row['ninth most downloaded article'], row['tenth most downloaded article']])
