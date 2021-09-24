# scrapes bobdylan.com/songs to get all lyrics

import requests
import sys,os
import argparse
from bs4 import BeautifulSoup

# config parameters
baseurl   = 'https://www.bobdylan.com/songs/'
basepath  = 'scrape'
basefile  = f'{basepath}/songs.html'

songlist  = []

# if songs.html does not exist, scrape it and save it
if not os.path.isfile(basefile):
    print(f'Loading {baseurl}')
    resp    = requests.get(baseurl)
    with open(basefile,'wt') as fout:
        for line in resp.text:
            fout.write(line)

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
for span in spans:
    links = span.find_all('a')
    for link in links:
        songlinks.append(str(link['href']))
        
assert (len(songlinks)==len(songnames)), ' len(songnames) != len(songlinks)'    
            


