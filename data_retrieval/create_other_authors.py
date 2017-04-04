import sqlite3 as db

conn = db.connect('../sqlite/scholarDB.db')
c = conn.cursor()
authors_ieee = c.execute('SELECT authors FROM ieee ORDER BY rowid').fetchall()
rowid_ieee = c.execute('SELECT rowid FROM ieee ORDER BY rowid').fetchall()
rowid_ieee = [id[0] for id in rowid_ieee]
authors_acm = c.execute('SELECT authors FROM acm ORDER BY rowid').fetchall()
rowid_acm = c.execute('SELECT rowid FROM acm ORDER BY rowid').fetchall()
rowid_acm = [id[0] for id in rowid_acm]
authors_dblp = c.execute('SELECT author FROM dblp ORDER BY rowid').fetchall()
rowid_dblp = c.execute('SELECT rowid FROM dblp ORDER BY rowid').fetchall()
rowid_dblp = [id[0] for id in rowid_dblp]
first_authors_ieee = [author[0].split(',')[0] for author in authors_ieee]
first_authors_acm = [author[0].split(',')[0] for author in authors_acm]
first_authors_dblp = [author[0].split(',')[0] for author in authors_dblp]
other_authors_ieee = [author[0].split(',')[1:] for author in authors_ieee]
other_authors_acm = [author[0].split(',')[1:] for author in authors_acm]
other_authors_dblp = [author[0].split(',')[1:] for author in authors_dblp]


count = 0
# Update ieee table
for index, row in enumerate(rowid_ieee):
    other_authors = ''
    # For each author in each row
    for a in other_authors_ieee[index]:
        other_authors += a
        if a != other_authors_ieee[index][-1]:
            other_authors += ','
    c.execute("UPDATE 'ieee' SET 'other authors'=?, 'authors'=? WHERE rowid=?", (other_authors, first_authors_ieee[index], int(row)))
    count += 1
    if count % 500 == 0:
        print(("Processed: ", count))

count = 0
# Update acm table
for index, row in enumerate(rowid_acm):
    other_authors = ''
    # For each author in each row
    for a in other_authors_acm[index]:
        other_authors += a
        if a != other_authors_acm[index][-1]:
            other_authors += ','
    c.execute("UPDATE 'acm' SET 'other authors'=?, 'authors'=? WHERE rowid=?", (other_authors, first_authors_acm[index], int(row)))
    count += 1
    if count % 500 == 0:
        print(("Processed: ", count))

count = 0
# Update dblp table
for index, row in enumerate(rowid_dblp):
    other_authors = ''
    # For each author in each row
    for a in other_authors_dblp[index]:
        other_authors += a
        if a != other_authors_dblp[index][-1]:
            other_authors += ','
    c.execute("UPDATE 'dblp' SET 'other authors'=?, 'author'=? WHERE rowid=?", (other_authors, first_authors_dblp[index], int(row)))
    count += 1
    if count % 500 == 0:
        print(("Processed: ", count))

conn.commit()
