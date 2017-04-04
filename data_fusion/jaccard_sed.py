import sqlite3
import editdistance
import re


path = '../sqlite/paperDB.db'
connection = sqlite3.connect(path)
output_file = 'jaccard_sed.txt'

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
                    s1 = list(re.sub(r'[^\w\s]|_', '', rows[i][0]).lower().strip().split())
                if rows[j][0] is None:
                    s2 = ''
                else:
                    s2 = list(re.sub(r'[^\w\s]|_', '', rows[j][0]).lower().strip().split())

                # add the shit here
                loop_times = min(len(s1), len(s2))
                for k in range(loop_times):
                    threshold = int(max(len(s1[k]), len(s2[k])) * 0.25)
                    distance = editdistance.eval(s1[k], s2[k])
                    if distance < threshold:
                        if len(s1[k]) > len(s2[k]):
                            s2[k] = s1[k]
                        else:
                            s1[k] = s2[k]
                s1 = set(s1)
                s2 = set(s2)
                intersection = len(s1.intersection(s2))
                union = len(s1.union(s2))
                jaccard_sim = float(intersection / union)
                if jaccard_sim >= 0.75:
                    f.write(str(i) + ' ' + str(j) + '\n')
                    print((str(i) + ' ' + str(j) + '\n'))
                    f.write('title1: ' + rows[i][0] + '\n')
                    print(('title1: ' + rows[i][0] + '\n'))
                    f.write('title2: ' + rows[j][0] + '\n')
                    print(('title2: ' + rows[j][0] + '\n'))
                    f.write('score: ' + str(float(intersection / union)) + '\n')
                    print(('score: ' + str(float(intersection / union)) + '\n'))
                    f.write('\n')
                    count += 1
        f.write('TOTAL COUNT: ' + str(count))
