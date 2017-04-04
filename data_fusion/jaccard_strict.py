import sqlite3
# import editdistance
import re


path = '../sqlite/paperDB.db'
connection = sqlite3.connect(path)
output_file = 'jaccard_strict.txt'

with connection:
    with open(output_file, 'w') as f:
        cursor = connection.cursor()
        cursor.execute('select title from papers')
        rows = cursor.fetchall()
        count = 0
        for i in range(len(rows)):
            for j in range(i + 1, len(rows)):
                # Remove punctuation and lower case
                if rows[i][0] is None:
                    s1 = ''
                else:
                    s1 = set(re.sub(r'[^\w\s]|_', '', rows[i][0]).lower().strip().split())
                if rows[j][0] is None:
                    s2 = ''
                else:
                    s2 = set(re.sub(r'[^\w\s]|_', '', rows[j][0]).lower().strip().split())
                intersection = len(s1.intersection(s2))
                union = len(s1.union(s2))
                jaccard_sim = float(intersection / union)
                if jaccard_sim >= 0.75:
                    f.write(str(i) + ' ' + str(j))
                    f.write('title1: ' + rows[i][0])
                    f.write('title2: ' + rows[j][0])
                    f.write('score: ', str(float(intersection / union)))
                    f.write('\n')
                    count += 1
        f.write('TOTAL COUNT: ' + str(count))
