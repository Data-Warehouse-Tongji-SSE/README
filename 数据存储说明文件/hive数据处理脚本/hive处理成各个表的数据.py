import datetime
import re
import json

with open('finalData9.txt','r',encoding='UTF-8') as preData,open('movie.txt','w',encoding='UTF-8') as movie,\
open('genres.txt','w',encoding='UTF-8') as genres,open('director.txt','w',encoding='UTF-8') as director,\
open('starring.txt','w',encoding='UTF-8') as starring,open('actor.txt','w',encoding='UTF-8') as actor,\
open('comment.txt','w',encoding='UTF-8') as comment:
    movieContents=['Title','VideoTime','Points','PointPersonNumber','totalNumber','Year','Month','Day','WeekDay']
    commentContents=['userId',"profileName","score"]
    line = preData.readline()
    n = 0
    while line:
        n = n + 1
        if n % 10000 == 0:
            print(n)
        text = json.loads(line)
        id=text['id']
        
        #movie数据
        movie.write(id)
        for content in movieContents:
            if content in text.keys():
                movie.write("<"+str(text[content]))
            else:
                movie.write("<"+"0")
        movie.write("\n")

        #genres数据
        if 'Genres' in text.keys():
            gens=text['Genres']
            for gen in gens:
                genres.write(id+'<'+str(gen)+'\n')

        #director数据
        if 'Director' in text.keys():
            dirs=text['Director']
            if isinstance(dirs,list):
                for dir in dirs:
                    director.write(id+'<'+str(dir)+'\n')
            else:
                Dirs=dirs.split(',')
                for dir in Dirs:
                    if dir != "":
                        director.write(id+'<'+str(dir)+'\n')
            

        #starring数据
        if 'Starring' in text.keys():
            stars=text['Starring']
            if isinstance(stars,list):
                for star in stars:
                    starring.write(id+'<'+str(star)+'\n')
            else:
                Stars=stars.split(',')
                for star in Stars:
                    if star != "":
                        starring.write(id+'<'+str(star)+'\n')

        #actor数据
        if 'Supporting actors' in text.keys():
            acts=text['Supporting actors']
            if isinstance(acts,list):
                for act in acts:
                    actor.write(id+'<'+str(act)+'\n')
            else:
                Acts=acts.split(',')
                for act in Acts:
                    if act != "":
                        actor.write(id+'<'+str(act)+'\n')

        #comment数据
        if 'Comments' in text.keys():
            coms=text['Comments']
            for com in coms:
                comment.write(id)
                for content in commentContents:
                    if content in com.keys():
                        comment.write("<"+str(com[content]))
                    else:
                        comment.write("<"+"")
                comment.write('\n')

                
        
        line = preData.readline()

print('finish')