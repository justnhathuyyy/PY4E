# Mixed test for Tuple & T
with open("mbox-short.txt") as file:
    count = dict()
    lines = [lines.split() for lines in file if lines.startswith("From ")]
    time = [line[-2] for line in lines]
    hour = [hours.split(":")[0] for hours in time]
    for x in hour:
        count[x] = count.get(x, 0) + 1
    for key,value in sorted(count.items()):
        print(key,value)

----
# Test for XML

import urllib.request, urllib.parse, urllib.error
import xml.etree.ElementTree as ET
import ssl
# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Enter link and read data
url1 = "http://py4e-data.dr-chuck.net/comments_42.xml"
url2 = "http://py4e-data.dr-chuck.net/comments_1762074.xml"
response = urllib.request.urlopen(url2)
string = response.read()

# Parse the XML data
data = ET.fromstring(string)

# Find the tag
comment = data.findall(".//comment")
print("Count is", len(comment))

# Take out all the names:
    # for item in comment:
        # print("Name is", item.find("name").text)
        # print("Count is", item.find("count").text)

print(sum(int(item.find("count").text) for item in comment))

----
# Test for using BeautifulSoup to read html, search for links, find tag

from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
import re

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def get_info():
    # Get input from users: position, counts
    position = int(input("Enter position "))
    max_count = int(input("Enter count "))
    return position, max_count

def link_url(link, position):
    # Take link and use urllib to open html link
    url = link
    html = urlopen(url, context=ctx).read()
    # Use bs4 to convert html -> string
    soup = BeautifulSoup(html, "html.parser")
    # Search for tag "a"
    tags = soup("a")
    a = []
    for tag in tags:
        # Take the link in each tag
        a.append(tag.get('href', None))
    print("Retrieving: ", a[position]tag

def homework():
    link = input("Enter first link ")
    position, max_count = get_info()
    while True:
        value = link_url(link,position-1)
        for count in range(max_count-1):
            if count < max_count:
                value = link_url(value,position-1)
                count += 1
                # print(count)
            elif count == max_count-1:
                print(value)
                break
        break

homework()

---
# READING JSON FILE TEST

from urllib.request import urlopen
import json
import ssl

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://py4e-data.dr-chuck.net/comments_1762075.json"
response = urlopen(url, context=ctx).read()
#response = requests.get(url)

info = json.loads(response)
print("Number of items:", len(info))
#num = []
#for x in info["comments"]:
    #num.append(x["count"])
#print(sum(num))

print(sum(x["count"] for x in info["comments"]))

---
# TEST FOR READ JSON FILE FOR GOOGLEMAPS API

import urllib.request, urllib.parse, urllib.error
import json
import ssl

api_key = False
# If you have a Google Places API key, enter it here
# api_key = 'AIzaSy___IDByT70'
# https://developers.google.com/maps/documentation/geocoding/intro

if api_key is False:
    api_key = 42
    serviceurl = 'http://py4e-data.dr-chuck.net/json?'
else :
    serviceurl = 'https://maps.googleapis.com/maps/api/geocode/json?'

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

while True:
    address = input('Enter location: ')
    if len(address) < 1: break

    parms = dict()
    parms['address'] = address
    if api_key is not False: parms['key'] = api_key
    url = serviceurl + urllib.parse.urlencode(parms)

    print('Retrieving', url)
    uh = urllib.request.urlopen(url, context=ctx)
    data = uh.read().decode()
    print('Retrieved', len(data), 'characters')

    try:
        js = json.loads(data)
    except:
        js = None

    if not js or 'status' not in js or js['status'] != 'OK':
        print('==== Failure To Retrieve ====')
        print(data)
        continue

    print(json.dumps(js, indent=4))

    #lat = js['results'][0]['geometry']['location']['lat']
    #lng = js['results'][0]['geometry']['location']['lng']
    #print('lat', lat, 'lng', lng)
    location = js['results'][0]['formatted_address']
    print(location)
    print("Place id ", js["results"][0]["place_id"])

---
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
