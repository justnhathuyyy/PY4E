# PY4E
Exams of PY4E, Uni of Michigan, Coursera

-----
# COURSE 4, WEEK 3, Count Email in Database
import sqlite3
import re

conn = sqlite3.connect('emaildb.sqlite')
# Creates a cursor object to interact with the database.
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Counts')

# creates a new table with two columns email and count.
cur.execute('''
CREATE TABLE Counts (org TEXT, count INTEGER)''')

fh = open("mbox.txt")

for line in fh:
    if line.startswith('From: '):
        org = re.findall('@(\S+)', line)[0]
        cur.execute('SELECT count FROM Counts WHERE org = ? ', (org,))
        row = cur.fetchone()
        if row is None:
            # If the ORG name does not exist, a new row is inserted into the Counts table with a count of 1.
            cur.execute('''INSERT INTO Counts (org, count)
                    VALUES (?, 1)''', (org,))
        else:
            # If the email address does exist, the count for that email address is updated by 1.
            cur.execute('UPDATE Counts SET count = count + 1 WHERE org = ?',
                        (org,))
        conn.commit()

sqlstr = 'SELECT org, count FROM Counts ORDER BY count DESC LIMIT 10'
for row in cur.execute(sqlstr):
    print(str(row[0]), row[1])

cur.close()
