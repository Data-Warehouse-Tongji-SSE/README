import json
import UnionFind
from ast import literal_eval
import re

with open('finalData7.txt','r',encoding='UTF-8') as data,open('finalData9.txt','w',encoding='UTF-8') as newData:
    line = data.readline()
    n = 0
    while line:
        n += 1
        if n % 10000 == 0:
            print(n)
        text = json.loads(line)
        title = text['Title']
        title = re.sub('\\(.*?\\)','',title)
        title = re.sub('\\[.*?\\]','',title)
        title = title.strip()
        text['Title'] = title
        if 'Supporting actors' in text.keys():
            actors = text['Supporting actors']
            if type(actors) is str:
                actors = actors.split(',')
            arr = []
            for actor in actors:
                if 'more\u2026' in actor:
                    actor = actor.replace('more\u2026','')
                actor = actor.strip()
                if actor not in arr:
                    arr.append(actor)
            text['Supporting actors'] = arr
        
        if 'Director' in text.keys():
            arr = []
            director = text['Director']
            dirs = director.split(',')
            for dir in dirs:
                dir = dir.strip()
                if dir not in arr:
                    arr.append(dir)
            text['Director'] = arr

        if 'Genres' in text.keys():
            arr = []
            genres = text['Genres']
            for x in genres:
                x = x.strip()
                if x not in arr:
                    arr.append(x)
            text['Genres'] = arr
            
        newData.write(json.dumps(text) + '\n')
        line = data.readline()

print('finish')