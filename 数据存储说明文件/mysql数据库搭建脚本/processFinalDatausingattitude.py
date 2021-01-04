import json
import csv

myMovieList = []
myMovieList1 = []
myPersonDict = {}
myGenresDict = {}
myUserDict = {}
myCommentList = []
myGenresRelationList = []
myDirectorRelationList = []
myStarringRelationList = []
mySupportingRelationList = []

outputFolder = "./Final_neo4j_Data/"
myCommentsPath = outputFolder + "comments.csv"

finalFile = open("./2.txt", "r+", encoding="utf-8", errors='ignore')
counter = 0
while True:
    cLine = finalFile.readline()
    counter += 1
    if counter % 10000 == 0:
        print(counter)
    if cLine:
        #d=cLine.replace("'","\"")
        #d=json.dumps(d)
        myList = json.loads(json.dumps(eval(cLine)))
        #print(myList['id'])
        try:
            product_id = myList['id']
        except(Exception):
            product_id = ""
        try:
            Title = myList['userId'].strip()
        except(Exception):
            Title = ""
        try:
            VideoTime = int(myList['attitude'])
        except(Exception):
            VideoTime = 0
        try:
            Points = float(myList['score'])
        except(Exception):
            Points = 0
        try:
            totalNumber = bool(myList['isSub'])
        except(Exception):
            totalNumber = 0 
        myCommentList.append([product_id, Title, Points,VideoTime,totalNumber])
    else:
        break
finalFile.close()

with open(myCommentsPath, 'w', newline='', encoding="utf-8", errors='ignore') as commentFile:
    spamwriter=csv.writer(commentFile, dialect='excel')
    spamwriter.writerow(["product_id", "user_id", "score","attitude","isSub"])
    for row in myCommentList:
        spamwriter.writerow(row)
        
