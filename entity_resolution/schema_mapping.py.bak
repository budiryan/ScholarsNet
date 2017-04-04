import sqlite3
import editdistance

table_names = ['arxiv', 'acm', 'dblp', 'ieee']
attribute_mappings = {}
connection = sqlite3.connect('../sqlite/scholarDB.db')
connection.row_factory = sqlite3.Row

for table in table_names:
    cursor = connection.execute('select * from ' + table)
    row = cursor.fetchone()
    attribute_mappings[table] = row.keys()

with open('edit_distance_output.txt', 'w') as output_file:
    # Create mapping from each of the table
    for i in range(len(table_names)):
        for j in range(i + 1, len(table_names)):
            attributes_table_1 = attribute_mappings[table_names[i]]
            attributes_table_2 = attribute_mappings[table_names[j]]
            output_file.write('Comparison between string distance of "' + table_names[i] + '" and "' + table_names[j] + '":\n')
            # Write the attribute name to file for the second dimension
            attribute_1_max_length = max([len(attribute_1) for attribute_1 in attributes_table_1])
            space_len = attribute_1_max_length * ' '
            output_file.write(space_len)
            for attribute in attributes_table_2:
                output_file.write('%*s  ' % (len(attribute), attribute))
            for attribute_1 in attributes_table_1:
                # First dimension
                output_file.write('\n')
                # Write the attribute name for the first dimension
                output_file.write('%*s' % (attribute_1_max_length, attribute_1))
                for attribute_2 in attributes_table_2:
                    # Second dimension
                    # output_file.write((str(editdistance.eval(attribute_1, attribute_2)).zfill(2) + '    '))
                    edit_distance = str(editdistance.eval(attribute_1, attribute_2)).zfill(2)
                    string_length = len(attribute_2)
                    output_file.write('%*s  ' % (string_length, edit_distance))
            output_file.write('\n\n')
