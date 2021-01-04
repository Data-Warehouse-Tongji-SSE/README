import json
import csv

myMovieList = []
myPersonDict = {}
myGenresDict = {}
myUserDict = {}
myCommentList = []
myGenresRelationList = []
myDirectorRelationList = []
myStarringRelationList = []
mySupportingRelationList = []
myCooperationRelationDict = {}

outputFolder = "./Final_neo4j_Data/"
myMoviePath = outputFolder + "movies.csv"
myPersonPath = outputFolder + "persons.csv"
myGenresPath = outputFolder + "genres.csv"
myUsersPath = outputFolder + "users.csv"
myCommentsPath = outputFolder + "comments.csv"
myGenresRelationPath = outputFolder + "genres_relation.csv"
myDirectorRelationPath = outputFolder + "director_relation.csv"
myStarringRelationPath = outputFolder + "starring_relation.csv"
mySupportingRelationPath = outputFolder + "supporting_relation.csv"
myCooperationRelationPath = outputFolder + "cooperation_relation.csv"

finalFile = open("./finalData.txt", "r+", encoding="utf-8", errors='ignore')
counter = 0
while True:
    cLine = finalFile.readline()
    counter += 1
    if counter % 1000 == 0:
        print(counter)
    if cLine:
        myList = json.loads(cLine)
        movie_id = myList["id"]
        try:
            Title = myList["Title"].strip()
        except(Exception):
            Title = ""
        if Title == "":
            Title = " "
        try:
            VideoTime = int(myList["VideoTime"])
        except(Exception):
            VideoTime = 0
        try:
            Points = float(myList["Points"])
        except(Exception):
            Points = 0
        try:
            PointPersonNumber = int(myList["PointPersonNumber"])
        except(Exception):
            PointPersonNumber = 0
        try:
            totalNumber = int(myList["totalNumber"])
        except(Exception):
            totalNumber = 0            
        try:
            Year = int(myList["Year"])
        except(Exception):
            Year = 0  
        try:
            Month = int(myList["Month"])
        except(Exception):
            Month = 0 
        try:
            Day = int(myList["Day"])
        except(Exception):
            Day = 0 
        try:
            WeekDay = int(myList["WeekDay"])
        except(Exception):
            WeekDay = 0
        myMovieList.append([movie_id, Title, VideoTime, Points, PointPersonNumber, totalNumber, Year, Month, Day, WeekDay])
        try:
            Genres = myList["Genres"]
            for genres in Genres:
                genres = genres.strip()
                tmp = len(myGenresDict)
                if genres not in myGenresDict.keys():
                    myGenresDict[genres] = tmp
                else:
                    tmp = myGenresDict[genres]
                myGenresRelationList.append([movie_id, tmp])
        except(Exception):
            pass
        try:
            Director = myList["Director"]
            tmpDirectorList = []
            for director in Director:
                director = director.strip()
                if director == "":
                    director = " "
                tmp = len(myPersonDict)
                if director not in myPersonDict.keys():
                    myPersonDict[director] = tmp
                else:
                    tmp = myPersonDict[director]
                myDirectorRelationList.append([movie_id, tmp])
                if tmp not in myCooperationRelationDict.keys():
                    myCooperationRelationDict[tmp] = {}
                tmpDirectorList.append(tmp)
        except(Exception):
            pass
        try:
            Starring = myList["Starring"]
            for starring in Starring:
                starring = starring.strip()
                if starring == "":
                    starring = " "
                tmp = len(myPersonDict)
                if starring not in myPersonDict.keys():
                    myPersonDict[starring] = tmp
                else:
                    tmp = myPersonDict[starring]
                myStarringRelationList.append([movie_id, tmp])
                for tmpDirector in tmpDirectorList:
                    if tmp not in myCooperationRelationDict[tmpDirector].keys():
                        myCooperationRelationDict[tmpDirector][tmp] = 1
                    else:
                        myCooperationRelationDict[tmpDirector][tmp] += 1
        except(Exception):
            pass
        try:
            Supporting = myList["Supporting actors"]
            for supporting in Supporting:
                supporting = supporting.strip()
                if supporting == "":
                    supporting = " "
                tmp = len(myPersonDict)
                if supporting not in myPersonDict.keys():
                    myPersonDict[supporting] = tmp
                else:
                    tmp = myPersonDict[supporting]
                mySupportingRelationList.append([movie_id, tmp])
                for tmpDirector in tmpDirectorList:
                    if tmp not in myCooperationRelationDict[tmpDirector].keys():
                        myCooperationRelationDict[tmpDirector][tmp] = 1
                    else:
                        myCooperationRelationDict[tmpDirector][tmp] += 1                
        except(Exception):
            pass
        try:
            Comments = myList["Comments"]
            for comment in Comments:
                userId = comment["userId"]
                profileName = comment["profileName"].strip()
                if profileName == "":
                    profileName = " "
                score = float(comment["score"])
                myCommentList.append([movie_id, userId, score])
                myUserDict[userId] = profileName
        except(Exception):
            pass                
    else:
        break
finalFile.close()

with open(myMoviePath, 'w', newline='', encoding="utf-8", errors='ignore') as movieFile:
    spamwriter=csv.writer(movieFile, dialect='excel')
    spamwriter.writerow(["id", "Title", "VideoTime", "Points", "PointPersonNumber", "totalNumber", "Year", "Month", "Day", "WeekDay"])
    for row in myMovieList:
        spamwriter.writerow(row)

with open(myPersonPath, 'w', newline='', encoding="utf-8", errors='ignore') as personFile:
    spamwriter=csv.writer(personFile, dialect='excel')
    spamwriter.writerow(["person_id", "name"])
    for key, value in myPersonDict.items():
         spamwriter.writerow([value, key])

with open(myGenresPath, 'w', newline='', encoding="utf-8", errors='ignore') as genresFile:
    spamwriter=csv.writer(genresFile, dialect='excel')
    spamwriter.writerow(["genres_id", "type"])
    for key, value in myGenresDict.items():
         spamwriter.writerow([value, key])
         
with open(myUsersPath, 'w', newline='', encoding="utf-8", errors='ignore') as usersFile:
    spamwriter=csv.writer(usersFile, dialect='excel')
    spamwriter.writerow(["user_id", "username"])
    for key, value in myUserDict.items():
         spamwriter.writerow([key, value])
         
with open(myCommentsPath, 'w', newline='', encoding="utf-8", errors='ignore') as commentFile:
    spamwriter=csv.writer(commentFile, dialect='excel')
    spamwriter.writerow(["movie_id", "user_id", "score"])
    for row in myCommentList:
        spamwriter.writerow(row)
        
with open(myGenresRelationPath, 'w', newline='', encoding="utf-8", errors='ignore') as genresRelationFile:
    spamwriter=csv.writer(genresRelationFile, dialect='excel')
    spamwriter.writerow(["movie_id", "genres_id"])
    for row in myGenresRelationList:
        spamwriter.writerow(row)

with open(myDirectorRelationPath, 'w', newline='', encoding="utf-8", errors='ignore') as directorRelationFile:
    spamwriter=csv.writer(directorRelationFile, dialect='excel')
    spamwriter.writerow(["movie_id", "director_id"])
    for row in myDirectorRelationList:
        spamwriter.writerow(row)
        
with open(myStarringRelationPath, 'w', newline='', encoding="utf-8", errors='ignore') as starringRelationFile:
    spamwriter=csv.writer(starringRelationFile, dialect='excel')
    spamwriter.writerow(["movie_id", "starring_id"])
    for row in myStarringRelationList:
        spamwriter.writerow(row)

with open(mySupportingRelationPath, 'w', newline='', encoding="utf-8", errors='ignore') as supportingRelationFile:
    spamwriter=csv.writer(supportingRelationFile, dialect='excel')
    spamwriter.writerow(["movie_id", "supporting_id"])
    for row in mySupportingRelationList:
        spamwriter.writerow(row)
        
with open(myCooperationRelationPath, 'w', newline='', encoding="utf-8", errors='ignore') as cooperationRelationFile:
    spamwriter=csv.writer(cooperationRelationFile, dialect='excel')
    spamwriter.writerow(["director_id", "actor_id", "cooperation_times"])
    for key, value in myCooperationRelationDict.items():
        for innerKey, innerValue in value.items():
            spamwriter.writerow([key, innerKey, innerValue])