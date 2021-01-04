from bs4 import BeautifulSoup
from urllib import request
import requests
import urllib.error
import time
import socket
import html5lib
import random

ok = open(r"ok.txt",'a',encoding='utf-8')
finish = open(r"finished.txt",'a',encoding='utf-8')
with open(r"id.txt",encoding='utf-8') as f:
    id = f.readline().replace('\n','')
    n = 0
    # 不同的代理IP,代理ip的类型必须和请求url的协议头保持一
    with open(r"proxy.txt",encoding='utf-8') as pro:
        line=pro.readline().replace('\n','')
        proxy_list = 'http://localhost:9000/get'
        proxy_list.append(line)
    while id:
        n = n + 1
        if n % 10000==0:
            print(n)
        url = "https://www.amazon.com/-/zh/dp/" + id #拼接字符串
        #设置header
        from fake_useragent import UserAgent
        ua=UserAgent()
        headers = {
            'User-Agent': ua.random
        }

        # 随机获取代理IP
        proxy = random.choice(proxy_list)    
        try: 
            req = requests.get(url=url,headers=headers,proxies=proxy).text
            with open(f'{n}_{id}.html','w',encoding='UTF-8') as writeDown:
                writeDown.write(req)
        except urllib.error.HTTPError:
            print(f'{id} 404')
            id = f.readline().replace('\n','')
            continue
        except socket.timeout:
            continue