#!/usr/bin/env python3.4

import requests, os, time, sys
sys.path.append('/home/morgan/Envs/ticket_search/lib/python3.4/site-packages')
from bs4 import BeautifulSoup

PATH = '/home/morgan/Envs/ticket_search/CT_subreddit_list.txt'
if os.path.exists(PATH):
    with open(PATH) as f:
        dataList = f.read().split('\n')
else:
    dataList = []

LOGPATH = '/home/morgan/Envs/ticket_search/CT_SR_log.txt'
if os.path.exists(LOGPATH):
    with open(LOGPATH) as a:
        logList = a.read().split('\n')
else:
    logList = []

new_posts = 0

URL = '''https://www.reddit.com/r/CONCERTTICKETS/new/'''
BASE = '''https://www.reddit.com'''

response = requests.get(URL)

soup = BeautifulSoup(response.content, 'html.parser')
print(soup.prettify())
for listing in soup.find_all('p', {'class':'title'}):
    data_id = listing['href'][27:32]
    print(listing.text)
    if 'EDC' in listing.text.upper():
        new_posts += 1
        dataList.append(data_id)
        link_end = listing['href']
        url = BASE + link_end
        TEXT = str(listing.text+'\n'+url+'\n')
        sys.stdout.write(TEXT)

if new_posts > 0:
    with open(PATH, 'w') as f:
        data = '\n'.join(dataList)
        f.write(data)
else:
    with open(LOGPATH, 'w') as a:
        logList.append('No new posts as of %s' % (time.strftime('%c')))
        log = '\n'.join(logList)
        a.write(log)
