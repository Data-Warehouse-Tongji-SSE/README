from bs4 import BeautifulSoup
import os
import lxml
import json
from multiprocessing import Process, Pool, Manager, Queue

def handleMovie(bs,id):
    title = None
    videoTime = None
    showTime = None
    director = None
    starring = None
    supportingActors = None
    Genres = None
    points = None
    personNumber = None
    starsTable = None

    data = {'id':id}
    logo = bs.find(name='a',attrs={'class':'av-retail-m-nav-text-logo'})
    # 信息：电影名称、播放时间、上映时间、导演、主演、配角、类型、用户评分&评分人数、用户评星
    if logo:#是PV页面
        # 电影名称
        title = bs.find(name='h1',attrs={'data-automation-id':'title'})
        if title:
            title = title.get_text().strip()
            data['Title'] = title

        #播放时间
        videoTime = bs.find(name='span',attrs={'data-automation-id':'runtime-badge'})
        if videoTime:
            videoTime = videoTime.get_text()
            data['VideoTime'] = videoTime

        #上映时间
        showTime = bs.find(name='span',attrs={'data-automation-id':'release-year-badge'})
        if showTime:
            showTime = showTime.get_text()
            data['ShowTime'] = showTime

        #导演
        director = bs.find(name='span',text='Directors')
        if director:
            director = director.parent.next_sibling.get_text()# 导演名字
            data['Director'] = director
        
        #主演
        starring = bs.find(name='span',text='Starring')
        if starring: 
            starring = starring.parent.next_sibling.get_text()# 主演名字
            data['Starring'] = starring
        
        #配角
        supportingActors = bs.find(name='span',text='Supporting actors')
        if supportingActors:
            supportingActors = supportingActors.parent.next_sibling.get_text()#配角名字
            data['Supporting actors'] = supportingActors

        #类型
        Genres = bs.find(name='span',text='Genres')
        if Genres:
            Genres = Genres.parent.next_sibling.get_text()#类型名称
            Genres = Genres.split(',')
            genres = []
            for i in Genres:
                if i not in genres:
                    genres.append(i)
            data['Genres'] = genres
        
        #用户评分
        points = bs.find(name='span',attrs={'data-hook':'rating-out-of-text'})
        if points:#分数
            points = points.get_text().strip().split(' ')[0]
            data['Points'] = points
        personNumber = bs.find(name='span',attrs={'class':'a-size-base a-color-secondary'})
        if personNumber:#评分人数
            personNumber = personNumber.get_text().strip().split(' ')[0]
            data['PointPersonNumber'] = personNumber

        #用户评星
        starsTable = bs.findAll(name='table',attrs={'id':'histogramTable'})
        if starsTable:
            starsTable = starsTable[1]
            starsComment = {}
            for stars in starsTable.contents:
                if stars == '\n':continue
                starCount = stars.contents[1].contents[1].get_text().strip()
                starPercent = stars.contents[5].contents[3].get_text().strip()
                starsComment[starCount] = starPercent
            data['Stars'] = starsComment

        #其他形式
        otherFormats = bs.find(name='div',attrs={'data-automation-id':'other-formats'})
        if otherFormats:
            formats = []
            for f in otherFormats.findAll('a'):
                formats.append(f['href'][4:14])
            data['otherFormats'] = formats
        
        rated = bs.find(name='span',attrs={'data-automation-id':'rating-badge'})
        if videoTime:
            mint=videoTime.split(' ')[0]
        if rated:
            rated = rated.contents[0].get_text().strip()
            if 'Unrated' not in rated:
                if 'Unrated' not in rated:#如果有分级
                    if videoTime and ('h' in videoTime or int(mint.split('m')[0]) >= 15):
                        return data
                else:
                    if videoTime and ('h' in videoTime or int(mint.split('m')[0]) >= 50) and (director or starring):# 判断标准：超过1小时，有导演或主演或演员
                        return data

        seasons = bs.find(name='div',attrs={'class':'dv-node-dp-seasons'})# 是否分季
        
        if videoTime and ('h' in videoTime or int(mint.split['m'][0]) >= 50) and (director or starring) and seasons is None:# 判断标准：超过1小时，有导演或主演或演员
            return data
    
    else:
        # 信息：电影名称、播放时间、上映时间、导演、主演、配角、类型、用户评分&评分人数、用户评星
        #名称
        title = bs.find(name='span',attrs={'id':'productTitle'})
        if title:
            title = title.get_text().strip()
            data['Title'] = title

        productDetails = bs.findAll(name='div',attrs={'id':'detailBullets_feature_div'})#产品细节
        if productDetails:
            productDetails = productDetails[-1]
            ul = productDetails.contents[1]
            for li in ul.contents:
                if li == '\n':continue
                text = li.contents[0].contents[1].get_text()
                #播放时间
                if 'Run time' in text:
                    videoTime = li.contents[0].contents[3].get_text().strip()
                    data['VideoTime'] = videoTime

                #上映时间
                if 'Release date' in text:
                    showTime = li.contents[0].contents[3].get_text().strip()
                    data['ShowTime'] = showTime

                #导演
                if 'Director' in text:
                    director = li.contents[0].contents[3].get_text().strip()
                    data['Director'] = director

                #主演
                if 'Starring' in text:
                    starring = li.contents[0].contents[3].get_text().strip()
                    data['Starring'] = starring

                #演员
                if 'Actors' in text:
                    supportingActors = li.contents[0].contents[3].get_text().strip()
                    supportingActors = supportingActors.split(',')
                    actors = []
                    for actor in supportingActors:
                        actors.append(actor)
                    data['Supporting actors'] = actors

        #类型
        Genres = bs.find(name='ul',attrs={'class':'a-unordered-list a-nostyle a-vertical zg_hrsr'})
        if Genres:
            styles = []
            Genres = Genres.findAll('a')
            for style in Genres:
                text = style.get_text().strip()
                if '(' in text:
                    text = text.split('(')[0].strip()
                if '&' in text:
                    text = text.split('&')
                    for i in text:
                        i = i.strip()
                        if ' ' in i:
                            j = i.split(' ')[0]
                            styles.append(j)
                        else: styles.append(i)
                elif ' ' in text:
                    j = text.split(' ')[0]
                    styles.append(j)
                elif 'DVD' not in text: styles.append(text)
            otherStyle = bs.findAll(name='a',attrs={'class':'a-link-normal a-color-tertiary'})[-1].get_text().strip()
            if '&' in otherStyle:
                otherStyle = otherStyle.split('&')
                for other in otherStyle:
                    if other not in styles:
                        styles.append(other)
            data['Genres'] = styles
        
        #用户评分
        points = bs.find(name='span',attrs={'data-hook':'rating-out-of-text'})
        if points:#分数
            points = points.get_text().strip().split(' ')[0]
            data['Points'] = points
        personNumber = bs.find(name='div',attrs={'data-hook':'total-review-count'})
        if personNumber:#评分人数
            personNumber = personNumber.contents[0].get_text().strip().split(' ')[0]
            data['PointPersonNumber'] = personNumber
        
        #用户评星
        starsTable = bs.findAll(name='table',attrs={'id':'histogramTable'})
        if starsTable:
            starsTable = starsTable[1]
            starsComment = {}
            for stars in starsTable.contents:
                if stars == '\n':continue
                starCount = stars.contents[1].contents[1].get_text().strip()
                starPercent = stars.contents[5].contents[3].get_text().strip()
                starsComment[starCount] = starPercent
            data['Stars'] = starsComment
        
        #其他形式
        otherFormats = bs.findAll(name='ul',attrs={'class':'a-unordered-list a-nostyle a-button-list a-horizontal'})[1]
        if otherFormats:
            formats = []
            aTag = otherFormats.findAll(name='a')
            for f in aTag:
                link = f['href']
                if link == 'javascript:void(0)':continue
                index = link.find('dp')
                newId = link[index+3:index+13]
                if newId != id:
                    formats.append(newId)
            data['otherFormats'] = formats
        
        #其他选择
        options = bs.find(name='div',attrs={'id':'twister'})
        if options:
            additionalOptions = []
            options = options.findAll(name='span',attrs={'data-action':'tmm-see-more-editions-click'})
            for option in options:
                newOption = option['data-tmm-see-more-editions-click']
                newOption = json.loads(newOption)['metabindingUrl']
                if newOption == '#':continue
                index = newOption.find('dp')
                newId = newOption[index+3:index+13]
                if newId not in additionalOptions and newId not in formats:
                    additionalOptions.append(newId)
            data['AdditionalOptions'] = additionalOptions

        rated = bs.find(name='div',attrs={'class':'a-box a-box-thumbnail'})
        if videoTime:
            mint=videoTime.split(' ')[0]
        if rated:
            rated = rated.contents[0]
            rated = rated.contents[3].get_text().strip()
            if 'Unrated' not in rated:#如果有分级
                if videoTime and ('h' in videoTime or int(mint.split('m')[0]) >= 15):
                    return data
            else:
                if videoTime and ('h' in videoTime or int(mint.split('m')[0]) >= 50) and (director or (starring and supportingActors)):# 判断标准：超过1小时，有导演或主演或演员
                    return data
        
        if videoTime and ('h' in videoTime or int(mint.split('m')[0]) >= 50) and (director or (starring or supportingActors)):# 判断标准：超过1小时，有导演或主演或演员
            return data 
    return False

def worker(i,queue):
    print(f"process {i} ready.")

    with open(f"{i}.txt", "a") as res, open(f"{i}.err", "a") as err ,open(f"{i}.not", "a") as no:
        n = 0
        while True:
            n = n + 1
            if n % 1000 == 0:
                print(n)
            line = queue.get(True)
            line = line.split(' ')
            with open(f'{line[1]}','r',encoding='UTF-8') as text:
                    html = text.read()
                    bs = BeautifulSoup(html,'lxml')#创建对象
                    try:
                        ans = handleMovie(bs,line[0])
                        if ans != False:
                            res.write(json.dumps(ans) +'\n')
                            res.flush()
                        else:
                            no.write(line[0]+'\n')
                            no.flush()

                    except Exception as e:
                        err.write(f'{line[0]} {e}\n')
                        err.flush()
            queue.task_done()

if __name__ == '__main__':
    processCount = os.cpu_count()
    print(f'processNumber: {processCount}')

    with Manager() as manager:
        queue = manager.Queue()
        pool = Pool(processCount)

        for i in range(processCount):
            pool.apply_async(worker, (i,queue))
        pool.close()

        
        for dirpath,dirname,filename in os.walk('D:\dataware'):#更改根目录
            for f in filename:
                queue.put(f+' '+f'{dirpath}\\{f}')

        pool.join()
