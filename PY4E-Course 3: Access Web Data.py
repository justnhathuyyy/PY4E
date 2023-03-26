# USING BEAUTIFULSOUP TO ACCESS HTML
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

# EXTRACT DATA FROM XML

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

---

# READ DATA FROM JSON

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