import sqlite3


path = '../sqlite/paperDB.db'
connection = sqlite3.connect('../sqlite/paperDB.db')
with connection:
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM papers')
    rows = cursor.fetchall()
    for row in rows:
        row = list(row)
        if row[-1] == 'arxiv':
            row[5] = row[5][0:4]
            cursor.execute('insert into papers2 values(?,?,?,?,?,?,?,?)', row)
        else:
            row[5] = row[5][-5:]
            cursor.execute('insert into papers2 values(?,?,?,?,?,?,?,?)', row)
connection.commit()
