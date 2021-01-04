import datetime
import re
import json

with open('finalData9.txt','r',encoding='UTF-8') as preData,open('dir_act_cooperation.txt','w',encoding='UTF-8') as DAC,\
open('act_act_cooperation.txt','w',encoding='UTF-8') as AAC:
    dac={}
    aac={}
    line = preData.readline()
    n = 0
    while line:
        n = n + 1
        if n % 10000 == 0:
            print(n)
        text = json.loads(line)
        #dir_act_relation
        if 'Director' in text.keys():
            dirs=text['Director']
            for dir in dirs:
                if dir not in dac.keys():
                    dac[dir]={}
                if 'Starring' in text.keys():
                    stars=text['Starring']
                    for star in stars:
                        if star not in dac[dir].keys():
                            dac[dir][star]=1
                        else:
                            dac[dir][star]+=1
                if 'Supporting actors' in text.keys():
                    acts=text['Supporting actors']
                    for act in acts:
                        if act not in dac[dir].keys():
                            dac[dir][act]=1
                        else:
                            dac[dir][act]+=1  
        #act_act_relation
        if 'Starring' in text.keys():
            stars=text['Starring']
            for star1 in stars:
                if star1 not in aac:
                    aac[star1]={}
                if 'Starring' in text.keys():
                    stars=text['Starring']
                    for star in stars:
                        if star not in aac[star1].keys():
                            aac[star1][star]=1
                        else:
                            aac[star1][star]+=1
                if 'Supporting actors' in text.keys():
                    acts=text['Supporting actors']
                    for act in acts:
                        if act not in aac[star1].keys():
                            aac[star1][act]=1
                        else:
                            aac[star1][act]+=1
        if 'Supporting actors' in text.keys():
            stars=text['Supporting actors']
            for star1 in stars:
                if star1 not in aac:
                    aac[star1]={}
                if 'Starring' in text.keys():
                    stars=text['Starring']
                    for star in stars:
                        if star not in aac[star1].keys():
                            aac[star1][star]=1
                        else:
                            aac[star1][star]+=1
                if 'Supporting actors' in text.keys():
                    acts=text['Supporting actors']
                    for act in acts:
                        if act not in aac[star1].keys():
                            aac[star1][act]=1
                        else:
                            aac[star1][act]+=1
        line = preData.readline()
    
    m = 0
    for key,value in dac.items():
        for key1,value1 in value.items():
            m = m + 1
            if m % 10000 == 0:
                print(m)
            DAC.write(key+'<'+key1+'<'+str(value1)+'\n')
    m = 0
    for key,value in aac.items():
        for key1,value1 in value.items():
            m = m + 1
            if m % 10000 == 0:
                print(m)
            if aac[key][key1] != 0 and key != key1 and key1 in aac.keys() and key in aac[key1].keys():
                aac[key1][key] = 0
                AAC.write(key+'<'+key1+'<'+str(value1)+'\n')
print('finish')