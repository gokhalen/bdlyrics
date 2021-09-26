import pandas as pd
import json
import matplotlib.pyplot as plt

jsonfile  = 'scrape/data.json.clean'
# dropwords = []
dropwords = ['the','and','a','in',\
             'to','that','it','on',\
             'be','is','but','was',\
             'of','for','no','they',\
             'so','can','with','from',\
             'if','are','this','as'
            ]
with open(jsonfile,'rt') as fin:
    bd_datalist = json.load(fin)

combined_songlyrics = ''

for bd_dict in bd_datalist:
    lyrics = bd_dict['songlyrics']
    # don't want to make new works by adding the first word to the last
    # word of previous song
    combined_songlyrics += '\n'+lyrics.lower()

# if 'alternate' in combined_songlyrics:
#    print('Screw up!')
wordlist = combined_songlyrics.split()
wordser  = pd.Series(wordlist)
wordser  = wordser[~wordser.isin(dropwords)]
counts   = pd.value_counts(wordser)

plt.figure()
counts[0:1000].plot(linewidth='4',
                    fontsize='16',
                    logy=True
                    )
plt.xlabel(xlabel='word',fontsize=16)
plt.ylabel(ylabel='number of times used (log scale)',fontsize=16)
plt.title(label='frequency of the 1000 most used words in Bob Dylan songs',fontsize=16)

'''
plt.figure()
counts[-8000:-7000].plot(linewidth='2',
                    xlabel='word',
                    ylabel='number of times used',
                    title='frequency of the 2000 least used words in Bob Dylan songs'
                    )
'''