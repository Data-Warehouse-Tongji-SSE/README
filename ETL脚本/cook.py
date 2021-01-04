# import datetime
# import re
# import json

# monthNames = {
#     "January": 1,
#     "February": 2,
#     "March": 3,
#     "April": 4,
#     "May": 5,
#     "June": 6,
#     "July": 7,
#     "August": 8,
#     "September": 9,
#     "October": 10,
#     "November": 11,
#     "December": 12,
# }


# def handleTime(time):
#     if time.isdigit():
#         return f"{time}-0-0"
#     mts = re.findall("(\w+) (\d+), (\d+)", time)
#     y = 0
#     m = 0
#     d = 0
#     if len(mts) > 0:
#         mts = mts[0]
#         y = int(mts[2])
#         if mts[0].isalpha():
#             m = monthNames[mts[0]]
#         else:
#             optMonth = re.findall(".*?(\d+).*?", mts[0])
#             if len(optMonth) > 0:
#                 m = int(optMonth[0])

#         d = int(mts[1])
#     return f"{y}-{m}-{d}"

# with open('finalData.txt','r',encoding='UTF-8') as preData,open('finalData2.txt','w',encoding='UTF-8') as data:
#     line = preData.readline()
#     n = 0
#     while line:
#         n = n + 1
#         if n % 10000 == 0:
#             print(n)
#         text = json.loads(line)
#         if 'ShowTime' in text.keys():
#             time = text['ShowTime']
#             newTime = handleTime(time)
#             number = newTime.split('-')
#             del text['ShowTime']
#             text['Year'] = number[0]
#             text['Month'] = number[1]
#             text['Day'] = number[2]
#             if number[1] != '0' and number[2] != '0':
#                 weekday = datetime.datetime(int(number[0]),int(number[1]),int(number[2])).weekday()
#             else:
#                 weekday = -1
#             text['WeekDay'] = str(weekday+1)
#         data.write(json.dumps(text) + '\n')
#         line = preData.readline()

# print('finish')

import json
import re

def handleTime(time):
    s = re.findall(r'(\d+|\D+)', time)
    matches = []
    for x in s:
        if x.isdigit():
            matches.append(int(x))
    return matches

with open('finalData2.txt','r',encoding='UTF-8') as preData,open('finalData5.txt','w',encoding='UTF-8') as data:
    line = preData.readline()
    n = 0
    while line:
        n = n + 1
        if n %10000 == 0:
            print(n)
        text = json.loads(line)
        if 'VideoTime' in text.keys():
            time = text['VideoTime']
            matches = handleTime(time)
            if len(matches) == 2:
                num = matches[0]*60 + matches[1]
            elif len(matches) == 1:
                if matches[0] <= 10:
                    num = matches[0] * 60
                else:
                    num = matches[0]
            text['VideoTime'] = num
        data.write(json.dumps(text) + '\n')
        line = preData.readline()

print('finish')

