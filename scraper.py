# scrapes bobdylan.com/songs to get all lyrics

import requests
import sys,os
import argparse


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

            


