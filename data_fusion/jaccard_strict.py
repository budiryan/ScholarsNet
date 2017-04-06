import sqlite3
# import editdistance
import re


path = '../sqlite/paperDB.db'
connection = sqlite3.connect(path)
output_file = 'jaccard_strict.txt'

with open(output_file, 'w') as f:
    cursor = connection.cursor()
    cursor.execute('select title from papers')
    rows = cursor.fetchall()
    count = 0
    for i in range(len(rows)):
        for j in range(i + 1, len(rows)):
            # Remove punctuation and lower case
            if rows[i][0] is None:
                s1 = set('')
            else:
                s1 = set(re.sub(r'[^\w\s]|_', '', rows[i][0]).lower().strip().split())
            if rows[j][0] is None:
                s2 = set('')
            else:
                s2 = set(re.sub(r'[^\w\s]|_', '', rows[j][0]).lower().strip().split())
            intersection = len(s1.intersection(s2))
            union = len(s1.union(s2))
            try:
                jaccard_sim = float(intersection / union)
            except ZeroDivisionError:
                jaccard_sim = 0  # 2 empty strings concatenated together lel, useless!
            if jaccard_sim >= 0.75:
                f.write(str(i) + ' ' + str(j) + '\n')
                print(str(i) + ' ' + str(j) + '\n')

                if rows[i][0] is None:
                    f.write('title1: null' + '\n')
                    print('title1: null' + '\n')
                else:
                    f.write('title1: ' + rows[i][0] + '\n')
                    print('title1: ' + rows[i][0] + '\n')

                if rows[j][0] is None:
                    f.write('title2: null' + '\n')
                    print('title2: null' + '\n')
                else:
                    f.write('title2: ' + rows[j][0] + '\n')
                    print('title2: ' + rows[j][0] + '\n')

                f.write('score: ' + str(jaccard_sim) + '\n')
                print('score: ' + str(jaccard_sim) + '\n')
                f.write('\n')
                print('\n')
                count += 1
    f.write('TOTAL COUNT: ' + str(count))
