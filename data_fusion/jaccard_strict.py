import sqlite3
import re
import json


path = '../sqlite/paperDB.db'
connection = sqlite3.connect(path)
output_file = 'jaccard_strict2.json'

cursor = connection.cursor()
cursor.execute('select * from papers')
rows = cursor.fetchall()
count = 0
result_array = []
for i in range(len(rows)):
    for j in range(i + 1, len(rows)):
        if i != j:
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
            if jaccard_sim >= 0.9:
                print(str(i) + ' ' + str(j) + '\n')

                if rows[i][0] is None:
                    print('title1: null' + '\n')
                else:
                    print('title1: ' + rows[i][0] + '\n')

                if rows[j][0] is None:
                    print('title2: null' + '\n')
                else:
                    print('title2: ' + rows[j][0] + '\n')

                print('score: ' + str(jaccard_sim) + '\n')
                print('\n')
                count += 1
                result_array.append(
                    {
                        "i": i,
                        "title1": rows[i][0],
                        "url1": rows[i][4],
                        "j": j,
                        "title2": rows[j][0],
                        "url2": rows[j][4],
                        "score": jaccard_sim,
                        "count": count
                    }
                )
                if count % 1 == 0:
                    with open(output_file, 'w') as f:
                        json.dump(result_array, f, indent=4)
