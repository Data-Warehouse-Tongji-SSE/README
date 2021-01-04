import json

with open('newComments2.txt','r',encoding='UTF-8') as comments,open('finalData4.txt','w',encoding='UTF-8') as data:
    info = {}
    n = 0
    line = comments.readline()
    while line:
        n = n + 1
        text = json.loads(json.dumps(eval(line)))
        id = text['id']
        user = {}
        user['userId'] = text['userId']
        user['profileName'] = text['profileName']
        user['score'] = text['score']
        if id in info.keys():
            info[id].append(user)
        else:
            info[id] = [user]
        if n % 250000 == 0:# 避免内存爆炸和泄露
            print(n)
            line = comments.readline()
            while line and id == json.loads(json.dumps(eval(line)))['id']:
                n = n + 1
                text = json.loads(json.dumps(eval(line)))
                id = text['id']
                user = {}
                user['userId'] = text['userId']
                user['profileName'] = text['profileName']
                user['score'] = text['score']
                if id in info.keys():
                    info[id].append(user)
                else:
                    info[id] = [user]
                line = comments.readline()
            
            with open('none.txt','r',encoding='UTF-8') as preData:
                x = 0
                preDataLine = preData.readline()
                while preDataLine:
                    x = x + 1
                    if x % 10000 == 0:print(x)
                    preDataText = json.loads(json.dumps(eval(preDataLine)))
                    preDataId = preDataText['id']
                    preDataLine = preDataLine.replace('\n','').strip()
                    if preDataLine in info.keys():
                        preDataText['Comments'] = info[preDataLine]
                        del info[preDataLine]
                        data.write(json.dumps(preDataLine) + '\n')
                    preDataLine = preData.readline()
        
        else:line = comments.readline()
    
    with open('none.txt','r',encoding='UTF-8') as preData:
        n = 0
        line = preData.readline()
        while line:
            n = n + 1
            if n % 10000 == 0:print(n)
            text = json.loads(json.dumps(eval(line)))
            id = text['id']
            if id in info.keys():
                text['Comments'] = info[id]
                data.write(json.dumps(text) + '\n')
            line = preData.readline()

print('finished')


#product/productId: B003AI2VGA
#review/userId: A141HP4LYPWMSR
#review/profileName: Brian E. Erland "Rainbow Sphinx"
#review/helpfulness: 7/7
#review/score: 3.0
#review/time: 1182729600
#review/summary: "There Is So Much Darkness Now ~ Come For The Miracle"
#review/text: Synopsis: On the daily trek from Juarez, Mexico to El Paso, Texas an ever increasing number of female workers are found raped and murdered in the surrounding desert. Investigative reporter Karina Danes (Minnie Driver) arrives from Los Angeles to pursue the story and angers both the local police and the factory owners who employee the undocumented aliens with her pointed questions and relentless quest for the truth.<br /><br />Her story goes nationwide when a young girl named Mariela (Ana Claudia Talancon) survives a vicious attack and walks out of the desert crediting the Blessed Virgin for her rescue. Her story is further enhanced when the "Wounds of Christ" (stigmata) appear in her palms. She also claims to have received a message of hope for the Virgin Mary and soon a fanatical movement forms around her to fight against the evil that holds such a stranglehold on the area.<br /><br />Critique: Possessing a lifelong fascination with such esoteric matters as Catholic mysticism, miracles and the mysterious appearance of the stigmata, I was immediately attracted to the '05 DVD release `Virgin of Juarez'. The film offers a rather unique storyline blending current socio-political concerns, the constant flow of Mexican migrant workers back and forth across the U.S./Mexican border and the traditional Catholic beliefs of the Hispanic population. I must say I was quite surprised by the unexpected route taken by the plot and the means and methods by which the heavenly message unfolds.<br /><br />`Virgin of Juarez' is not a film that you would care to watch over and over again, but it was interesting enough to merit at least one viewing. Minnie Driver delivers a solid performance and Ana Claudia Talancon is perfect as the fragile and innocent visionary Mariela. Also starring Esai Morales and Angus Macfadyen (Braveheart).