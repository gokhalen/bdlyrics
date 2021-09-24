# scrapes bobdylan.com/songs to get all lyrics

import requests
import sys,os
import argparse
import time
import json
import re

from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename

# config parameters
baseurl   = 'https://www.bobdylan.com/songs/'
basepath  = 'scrape'
basefile  = f'{basepath}/songs.html'
basejson  = f'{basepath}/data.json'

songlist  = []

# if songs.html does not exist, scrape it and save it
if not os.path.isfile(basefile):
    print(f'Loading {baseurl}')
    resp    = requests.get(baseurl)
    with open(basefile,'wt') as fout:
        fout.write(resp.text)

# read songs.html            
from bs4 import BeautifulSoup
with open(basefile) as fin:
    ll  = fin.readlines()

htmlstr = ''
for l in ll:
    htmlstr +=l
    
soup  = BeautifulSoup(htmlstr,'html.parser')
# https://stackoverflow.com/questions/16248723/how-to-find-spans-with-a-specific-class-containing-specific-text-using-beautiful
spans     = soup.find_all('span',{'class':'song'})
songnames = [span.get_text() for span in spans]
songlinks = []
filenames = []

# make links 
for span in spans:
    links = span.find_all('a')
    for link in links:
        songlinks.append(str(link['href']))
        
# make filenames
for name in songnames:
    filenames.append(sanitize_filename(name))

# check to see that there are not duplicates     
assert (len(songlinks)==len(songnames) == len(filenames) == len(set(songlinks)) == len(set(songnames)) == len(set(filenames)) \
),'length of songlinks,songnames,filenames is not same'

number_of_songs = len(songlinks)

print(f'{number_of_songs=}')

# breakpoint()
# save song info
dd = {'songlinks':songlinks,'songnames':songnames,'filenames':filenames}
with open(basejson,'wt') as fout:
    json.dump(dd,fout)


link  = songlinks[0]
fname = basepath+'/'+filenames[0]
if not os.path.isfile(fname):
    resp = requests.get(link)
    soup = BeautifulSoup(resp.text,'html.parser')
    lyrics = soup.find('div',{'class':'article-content lyrics'}).get_text()
    copylist = re.findall('copyright',lyrics,flags=re.IGNORECASE)
    print(lyrics)
    breakpoint()
    time.sleep(0.05)

