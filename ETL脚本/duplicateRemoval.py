import json
import UnionFind
from ast import literal_eval

# 先建立一个数组存入所有的id
arr = []
with open('data.txt','r',encoding='UTF-8') as file:
    line = file.readline()
    while line:
        text = json.loads(line)
        id = text['id']
        arr.append(id)
        line = file.readline()

# 根据上面的数组源数据建立并查集
myUnionFind = UnionFind.UnionFind(arr)

# 遍历源文件中商品，将商品存入并查集
with open('data.txt','r',encoding='UTF-8') as file:
    line = file.readline()
    n = 0
    while line:
        text = json.loads(line)
        id = text['id']

        if 'otherFormats' in text.keys():
            otherFormats = text['otherFormats']
            for format in otherFormats:
                if format in arr:
                    myUnionFind.union(id,format)

        if 'AdditionalOptions' in text.keys():
            addtionalOptions = text['AdditionalOptions']
            for option in addtionalOptions:
                if option in arr:
                    myUnionFind.union(id,option)
        n = n + 1
        if n%500 == 0:
            print(n)
        line = file.readline()

components = list(myUnionFind.components())
print('totalNumber:',len(components))

with open('newComponent.txt','a',encoding='UTF-8') as com:
    com.write(str(components))

cnt = {}

with open('newComponent.txt','r') as text:
    line = text.readline()
    components = literal_eval(line)

for component in components:
    l = list(component)
    item = l[0]
    cnt[item] = len(l)

with open('newNumber.txt','a') as num:
    num.write(json.dumps(cnt)+'\n')

# 遍历dict，根据index按行读取源文件，加入一个数字字段表示该电影有几个不同的版本（一部电影的不同版本各种信息相同），写入新文件

with open('newNumber.txt','r') as num:
    line = num.readline()
    cnt = json.loads(line)

with open('newData2.txt','a') as data,open('data.txt','r') as preData:
    line = preData.readline()
    n = 0
    while line:
        n = n + 1
        text = json.loads(line)
        id = text['id']
        if id in cnt.keys():
            text['totalNumber'] = cnt[id]
            data.write(json.dumps(text) + '\n')
        if n % 500 == 0:
            print(n)
            print(len(cnt))
        line = preData.readline()

print('finish')