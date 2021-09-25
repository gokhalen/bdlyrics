import json
import re
import sys
# config
jsonfile  = 'scrape/data.json'
jsonclean = 'scrape/data.json.clean'
processed = []


# functions and classes



def remove_punc(lyrics_str):
    '''
    removes '?',',' and other punc from text 
    '''
    puncs = ['?',',',')','(']
    out   = lyrics_str
    for punc in puncs:
        out = out.replace(punc,'')

    return out

def remove_copyright(lyrics_str,songname):
    '''
    removes copyright message from the lyrics
    this is an interactive function
    '''

    songlength = len(lyrics_str)
    out = lyrics_str

    # https://stackoverflow.com/questions/3519565/find-the-indexes-of-all-regex-matches    
    copyiter  = re.finditer('copyright',lyrics_str,flags=re.IGNORECASE)
    copystart = [ m.start(0) for m in copyiter ]

    if len(copystart) not in [0,1]:
        print(f'multiple copyrights detected for {songname=}')

    if copystart:
        start = copystart[0]
        copyrightratio = start/songlength
        print('-'*80+'\n')
        print(f'{copyrightratio=}'+'\n')
        print(out[start:])
        print('Enter any key to continue...')
        input()
        
    
    return out

def check_word(lyrics_str,songname,wordlist):
    for word in wordlist:
        worditer = re.finditer(word,lyrics_str,flags=re.IGNORECASE)
        wordstart = [ m.start(0) for m in worditer ]
        if len(wordstart) != 0:
            print(f'{word} detected in {songname}')

            # breakpoint()
        

def processing_message(songname):
    print('-'*80)
    print(f'Processing {songname}')
    print('-'*80)

# main program
with open(jsonfile,'rt') as fin:
    bd_datalist = json.load(fin)

for bd_dict in bd_datalist:
    songlink   = bd_dict['songlink']
    songname   = bd_dict['songname']
    songlyrics = bd_dict['songlyrics']
    
    # processing_message(songname)
    new_lyrics = remove_punc(songlyrics)
    new_lyrics = remove_copyright(new_lyrics,songname)
    check_word(new_lyrics,songname,['alternate version'])

    bd_dict['cleanlyrics'] = new_lyrics
    
    processed.append(bd_dict)
    
with open(jsonclean,'wt') as fout:
    json.dump(processed,fout,indent=4)
