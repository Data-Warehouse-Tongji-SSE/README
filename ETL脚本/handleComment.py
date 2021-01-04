import json
from ast import literal_eval
from textblob import TextBlob


with open('9.txt','r',encoding='UTF-8') as data,open('newComments2.txt','w',encoding='UTF-8') as effcomments,open('movies.txt','r',encoding='UTF-8',errors='ignore') as comments:
    arr = []
    line = data.readline()
    while line:
        text = json.loads(line)
        id = text['id']
        arr.append(id)
        line = data.readline()
    
    line = comments.readline()
    n = 0
    while line:
        n = n + 1
        if n % 10000 == 0:print(n)
        id = line.split(':')[-1].replace('\n','').strip()
        if len(id) != 10:
            line = comments.readline()
            while 'productId' not in line:
                line = comments.readline()
            continue
        if id in arr:
            comment = {}
            isFound = False
            comment['id'] = id
            line = comments.readline()
            while 'productId' not in line:
                if 'userId' in line:
                    userId = line.split(':')[-1].replace('\n','').strip()
                    comment['userId'] = userId
                    
                elif 'profileName' in line:
                    profileName = line.split(':')[-1].replace('\n','').strip()
                    comment['profileName'] = profileName 

                elif 'text' in line:
                    text = line.split(':')[-1].replace('\n','').strip()
                    testimonial = TextBlob(text)
                    attitude=0
                    isSub=True
                    polar=testimonial.sentiment.polarity
                    subject=testimonial.sentiment.subjectivity
                    if polar>0.15:
                        attitude=1
                    if polar<=0:
                        attitude=-1 
                    if subject<0.5:
                        isSub=False      
                    #print(testimonial.sentiment.polarity)
                    #print(testimonial.sentiment.subjectivity)
                    comment['attitude'] = attitude
                    comment['isSub'] = isSub
                    #comment['attitude1'] = polar
                    #comment['isSub1'] = subject


                elif 'score' in line:
                    score = line.split(':')[-1].replace('\n','').strip()
                    comment['score'] = score 

                if not isFound:
                    line = comments.readline()
                else:
                    while 'productId' not in line:
                        line = comments.readline()
            effcomments.write(str(comment)+'\n')
        else:
            line = comments.readline()
            while 'productId' not in line:
                line = comments.readline()
            while line and line.split(':')[-1].replace('\n','').strip() == id:
                n = n + 1
                if n % 10000 == 0:print(n)
                line = comments.readline()
                while 'productId' not in line:
                    line = comments.readline()
      
print('finished')

# with open('effectiveComments.txt','r',encoding='UTF-8') as comments,open('newComments.txt','w',encoding='UTF-8') as data:
#     line = comments.readline()
#     n = 0
#     while line:
#         n = n + 1
#         if n % 100000 == 0:print(n)
#         text = json.loads(json.dumps(eval(line)))
#         score = text['score']
#         if len(score) > 3:
#             text['score'] = '3.0'
#         encodedData = json.dumps(text)
#         data.write(encodedData+'\n')
#         data.flush()
#         line = comments.readline()


#product/productId: B003AI2VGA
#review/userId: A141HP4LYPWMSR
#review/profileName: Brian E. Erland "Rainbow Sphinx"
#review/helpfulness: 7/7
#review/score: 3.0
#review/time: 1182729600
#review/summary: "There Is So Much Darkness Now ~ Come For The Miracle"
#review/text: Synopsis: On the daily trek from Juarez, Mexico to El Paso, Texas an ever increasing number of female workers are found raped and murdered in the surrounding desert. Investigative reporter Karina Danes (Minnie Driver) arrives from Los Angeles to pursue the story and angers both the local police and the factory owners who employee the undocumented aliens with her pointed questions and relentless quest for the truth.<br /><br />Her story goes nationwide when a young girl named Mariela (Ana Claudia Talancon) survives a vicious attack and walks out of the desert crediting the Blessed Virgin for her rescue. Her story is further enhanced when the "Wounds of Christ" (stigmata) appear in her palms. She also claims to have received a message of hope for the Virgin Mary and soon a fanatical movement forms around her to fight against the evil that holds such a stranglehold on the area.<br /><br />Critique: Possessing a lifelong fascination with such esoteric matters as Catholic mysticism, miracles and the mysterious appearance of the stigmata, I was immediately attracted to the '05 DVD release `Virgin of Juarez'. The film offers a rather unique storyline blending current socio-political concerns, the constant flow of Mexican migrant workers back and forth across the U.S./Mexican border and the traditional Catholic beliefs of the Hispanic population. I must say I was quite surprised by the unexpected route taken by the plot and the means and methods by which the heavenly message unfolds.<br /><br />`Virgin of Juarez' is not a film that you would care to watch over and over again, but it was interesting enough to merit at least one viewing. Minnie Driver delivers a solid performance and Ana Claudia Talancon is perfect as the fragile and innocent visionary Mariela. Also starring Esai Morales and Angus Macfadyen (Braveheart).