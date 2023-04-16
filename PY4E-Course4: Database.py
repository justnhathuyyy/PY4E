# USE SQLITE3, COUNT EMAIL ADDRESS FROM A TXT FILE

import sqlite3
import re

conn = sqlite3.connect('emaildb.sqlite')
# Creates a cursor object to interact with the database.
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Counts')

# creates a new table with two columns email and count.
cur.execute('''
CREATE TABLE Counts (org TEXT, count INTEGER)''')

# sample: From: stephen.marquard@uct.ac.za
# org = re.findall("^From.*@(\S+)", lines)

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

---

# WEEK 3: # USE SQLLITE3, CREATE TABLE for Tracks, Albums, Artist, INSERT data, JOIN to view table

import xml.etree.ElementTree as ET
import sqlite3

conn = sqlite3.connect('trackdb.sqlite')
cur = conn.cursor()

# Make some fresh tables using executescript()
cur.executescript('''
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Track;
DROP TABLE IF EXISTS Genre;


CREATE TABLE Artist (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Genre (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Album (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id  INTEGER,
    title   TEXT UNIQUE
);

CREATE TABLE Track (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title TEXT  UNIQUE,
    album_id  INTEGER,
    genre_id  INTEGER,
    len INTEGER,
    rating INTEGER,
    count INTEGER
);
''')


fname = 'Library.xml'

# <key>Track ID</key><integer>369</integer>
# <key>Name</key><string>Another One Bites The Dust</string>
# <key>Artist</key><string>Queen</string>
def lookup(d, key):
    found = False
    for child in d:
        if found : return child.text
        if child.tag == 'key' and child.text == key :
            found = True
    return None

stuff = ET.parse(fname)
all = stuff.findall('dict/dict/dict')
print('Dict count:', len(all))
for entry in all:
    if (lookup(entry, 'Track ID') is None) : continue
    name = lookup(entry, 'Name')
    artist = lookup(entry, 'Artist')
    genre = lookup(entry, 'Genre')
    album = lookup(entry, 'Album')
    count = lookup(entry, 'Play Count')
    rating = lookup(entry, 'Rating')
    length = lookup(entry, 'Total Time')

    if name is None or artist is None or album is None or genre is None:
        continue

    print(name, artist, album, count, rating, length)

    cur.execute('''INSERT OR IGNORE INTO Artist (name) 
        VALUES ( ? )''', ( artist, ))
    cur.execute('SELECT id FROM Artist WHERE name = ? ', (artist, ))
    artist_id = cur.fetchone()[0]

    cur.execute(''' INSERT OR IGNORE INTO Genre (name)
        VALUES (?)''', ( genre, ))
    cur.execute('SELECT id FROM Genre WHERE name = ?', (genre, ))
    genre_id = cur.fetchone()[0]

    cur.execute('''INSERT OR IGNORE INTO Album (title, artist_id) 
        VALUES ( ?, ? )''', ( album, artist_id ) )
    cur.execute('SELECT id FROM Album WHERE title = ? ', (album, ))
    album_id = cur.fetchone()[0]

    cur.execute('''INSERT OR REPLACE INTO Track
        (title, album_id, genre_id, len, rating, count) 
        VALUES ( ?, ?, ?, ?, ?, ? )''',
        (name, album_id, genre_id, length, rating, count ) )

    conn.commit()

----
# WEEK 4: USE SQLITE3, LOAD JSON FILE, INSERT DATA INTO TABLES, MANY-TO-MANY RELATIONSHIPS

import json
import sqlite3

# Step1: Connect to SQL file, enable cursor
conn = sqlite3.connect("rosterdb.sqlite")
cur = conn.cursor()

# Step2: Drop table if already existed, and Create table
cur.executescript('''
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Course;
DROP TABLE IF EXISTS Member;

CREATE TABLE User (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT UNIQUE
);

CREATE TABLE Course (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title  TEXT UNIQUE
);

CREATE TABLE Member (
    user_id     INTEGER,
    course_id   INTEGER,
    role        INTEGER,
    PRIMARY KEY (user_id, course_id)
);
''')

# Step3: Open file, read file, and loads on json
file_name = 'roster_data.json'
data = open(file_name).read()
json_data = json.loads(data)
print(json_data)
print(len(json_data))

# Step4: Find needed items in json format, retrieve those items
# Zubair|si110|0
for item in json_data:
    name = item[0]
    title = item[1]
    role = item[2]
    # print(name, title, role)

    # Step5: Execute SQL to insert or ignore those items to tables in our database
    cur.execute('''INSERT OR IGNORE INTO User (name) VALUES (?)''', (name,))
    cur.execute('SELECT id FROM User WHERE name = ?', (name,))
    user_id = cur.fetchone()[0]

    cur.execute('''INSERT OR IGNORE INTO Course (title) VALUES (?)''', (title,))
    cur.execute('SELECT id FROM Course WHERE title = ?', (title,))
    course_id = cur.fetchone()[0]

    # Step6: Insert or replace data into many-to-many relationships table contains primary keys from 2 tables
    cur.execute('''INSERT OR REPLACE INTO
    Member (user_id, course_id, role) VALUES (?,?,?)''', (user_id, course_id, role))

    conn.commit()

# Step7: Execute JOIN to read

'''SELECT User.name, Course.title, Member.role FROM
	User JOIN Course JOIN Member
	ON User.id = Member.user_id and Course.id = Member.course_id
	ORDER BY User.name DESC, Course.title DESC, Member.role DESC LIMIT 2;
	SELECT 'XYZZY' || hex(User.name || Course.title || Member.role ) AS X FROM 
    User JOIN Member JOIN Course 
    ON User.id = Member.user_id AND Member.course_id = Course.id
    ORDER BY X LIMIT 1;'''


# USE SQLLITE3, CREATE TABLE for Tracks, Albums, Artist, INSERT data, JOIN to view table

import xml.etree.ElementTree as ET
import sqlite3

conn = sqlite3.connect('trackdb.sqlite')
cur = conn.cursor()

# Make some fresh tables using executescript()
cur.executescript('''
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Track;
DROP TABLE IF EXISTS Genre;


CREATE TABLE Artist (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Genre (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Album (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id  INTEGER,
    title   TEXT UNIQUE
);

CREATE TABLE Track (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title TEXT  UNIQUE,
    album_id  INTEGER,
    genre_id  INTEGER,
    len INTEGER,
    rating INTEGER,
    count INTEGER
);
''')


fname = 'Library.xml'

# <key>Track ID</key><integer>369</integer>
# <key>Name</key><string>Another One Bites The Dust</string>
# <key>Artist</key><string>Queen</string>
def lookup(d, key):
    found = False
    for child in d:
        if found : return child.text
        if child.tag == 'key' and child.text == key :
            found = True
    return None

stuff = ET.parse(fname)
all = stuff.findall('dict/dict/dict')
print('Dict count:', len(all))
for entry in all:
    if (lookup(entry, 'Track ID') is None) : continue
    name = lookup(entry, 'Name')
    artist = lookup(entry, 'Artist')
    genre = lookup(entry, 'Genre')
    album = lookup(entry, 'Album')
    count = lookup(entry, 'Play Count')
    rating = lookup(entry, 'Rating')
    length = lookup(entry, 'Total Time')

    if name is None or artist is None or album is None or genre is None:
        continue

    print(name, artist, album, count, rating, length)

    cur.execute('''INSERT OR IGNORE INTO Artist (name) 
        VALUES ( ? )''', ( artist, ))
    cur.execute('SELECT id FROM Artist WHERE name = ? ', (artist, ))
    artist_id = cur.fetchone()[0]

    cur.execute(''' INSERT OR IGNORE INTO Genre (name)
        VALUES (?)''', ( genre, ))
    cur.execute('SELECT id FROM Genre WHERE name = ?', (genre, ))
    genre_id = cur.fetchone()[0]

    cur.execute('''INSERT OR IGNORE INTO Album (title, artist_id) 
        VALUES ( ?, ? )''', ( album, artist_id ) )
    cur.execute('SELECT id FROM Album WHERE title = ? ', (album, ))
    album_id = cur.fetchone()[0]

    cur.execute('''INSERT OR REPLACE INTO Track
        (title, album_id, genre_id, len, rating, count) 
        VALUES ( ?, ?, ?, ?, ?, ? )''',
        (name, album_id, genre_id, length, rating, count ) )

    conn.commit()

