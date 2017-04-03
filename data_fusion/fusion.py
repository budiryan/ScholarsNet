import sqlite3


path = '../sqlite/paperDB.db'
connection = sqlite3.connect('scholarDB.db')
with connection:
    cursor = connection.cursor()
