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

# scrape base
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

# song properties
songnames  = [span.get_text() for span in spans]
songlinks  = []
songlyrics = []

# make links 
for span in spans:
    links = span.find_all('a')
    for link in links:
        songlinks.append(str(link['href']))
        
number_of_songs = len(songlinks)
print(f'{number_of_songs=}')

for ictr,link in enumerate(songlinks):
    #link  = songlinks[2]
    print(f'Retrieving and parsing {link=} {ictr} of {number_of_songs}')
    resp = requests.get(link)
    soup = BeautifulSoup(resp.text,'html.parser')
    lyrics = soup.find('div',{'class':'article-content lyrics'}).get_text()
    songlyrics.append(lyrics)
    # copylist = re.findall('copyright',lyrics,flags=re.IGNORECASE)
    # breakpoint()
    time.sleep(0.2)


# check to see that there are not duplicates     
assert (len(songlinks)==len(songnames) ==  \
        len(set(songnames)) == len(set(songlinks)) \
       ),'length of songlinks,songnames, is not same'
    
outlist = []

for _link, _name, _lyrics in zip(songlinks,songnames,songlyrics):
    dd = {'songlink':_link, 'songname':_name,'songlyrics':_lyrics}
    outlist.append(dd)

with open(basejson,'wt') as fout:
    json.dump(outlist,fout,indent=4)
