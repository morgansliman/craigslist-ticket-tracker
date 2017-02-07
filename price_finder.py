#!/usr/bin/env python3.4

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#
# Craigslist search scraper version 1.1
# Written by Morgan Sliman on Ubuntu 14.04.3 (Trusty Tahr)
#
# Future update (2.0):
#     -- optimized for ease of use
#     -- hopefully will include a web-app version
#
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

import requests, os, time, sys
sys.path.append('/home/morgan/Envs/ticket_search/lib/python3.4/site-packages')
from bs4 import BeautifulSoup
os.chdir('/home/morgan/Envs/ticket_search')

ERROR_PATH = '/home/morgan/Envs/ticket_search/connection_errors.txt'
PATH = '/home/morgan/Envs/ticket_search/datalist.txt'
LOG_PATH = '/home/morgan/Envs/ticket_search/empty_log.txt'


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#
# Below are the 'path checkers' for the datalist, empty_log,
# and connection_errors docs. 
#
# Yay comprehensions!
#
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
def get_contents(path):
    with open(path) as f:
        contents = f.read()
    return contents

errors = int(get_contents(ERROR_PATH)) if os.path.exists(ERROR_PATH) else 0
dataList = get_contents(PATH).split('\n') if os.path.exists(PATH) else []
logList = get_contents(LOG_PATH).split('\n') if os.path.exists(LOG_PATH) else []


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#
# The URL variable can be changed to reflect any desired search.
# However, other things will also need to be edited to
# reflect the change. 
#
# This should be made much more user friendly with a future update.
#
# ...side note: This error handling could DEFINITELY be done better.
#
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
URL = '''http://orlando.craigslist.org/search/tia?sort=rel&query=edc'''
BASE = 'http://orlando.craigslist.org'
new_posts = 0

def raise_error(error):
    if error == 3:
        with open(ERROR_PATH, 'w') as f:
            f.write('0')
        sys.stdout.write('The last three requests have failed. Please check connection.')
        sys.exit(1)
    else:
        with open(ERROR_PATH, 'w') as f:
            error += 1
            f.write(error)
        sys.exit(1)

try:
    response = requests.get(URL)
except:
    raise_error(errors)

soup = BeautifulSoup(response.content, 'html.parser')
for listing in soup.find_all('p',{'class':'row'}):
    data_id = listing['data-pid']
    if (listing.find('span',{'class':'price'}) != None) and (data_id not in dataList):
        price = listing.text[2:6]
        price = int(price)
        if price <= 340 and price >= 100:
            new_posts += 1
            dataList.append(data_id)
            link_end = listing.a['href']
            url = (BASE + link_end) if link_end.startswith('/tix') else ('http:' + link_end)
            TEXT = str(listing.text+'\n'+url+'\n')
            sys.stdout.write(TEXT)
            #print ('\n')

if new_posts > 0:
    with open(PATH, 'w') as f:
        data = '\n'.join(dataList)
        f.write(data)
else:
    with open('/home/morgan/Envs/ticket_search/empty_log.txt', 'w') as a:
        logList.append('No new posts as of %s' % (time.strftime('%c')))
        log = '\n'.join(logList)
        a.write(log)
