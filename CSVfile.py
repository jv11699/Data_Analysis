import DataUBVB as Data
import csv
import re

UBname = "UB" #Name to be used of who is serving
with open('DataofUB2018','w') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(["UB's score","Opponents Score","Who served that point","Opponent name","Match Number"]) #The title of the csv file.
    for i in range(0,Data.numOfMatches()): #The first for loops go through the matches
        lengthOfScores = len(Data.match(match_number=i, mode='score'))
        ubscore = Data.grabTeamScore(team='ub', match_number=i, mode='score')
        oppscore = Data.grabTeamScore(team = 'opponent', match_number = i, mode = 'score')
        oppname =  Data.match(i, 'opp name')
        SOdata = Data.match(i,'SO')
        scores = Data.match(match_number=i,mode='score')
        if (int(ubscore[0]) > 0): #whichever team scores first that means they were the one's who served.
            serve = UBname
        else:
            serve = oppname
        for x in range(0,lengthOfScores): #The second for loop goes through the scores
            writer.writerow([int(ubscore[x]),
                            int(oppscore[x]),
                            serve,
                            oppname,
                            i])
            #Checks the next score if its service over or a new set to change the state of who is serving.
            if (x < lengthOfScores - 1 and re.search(r'so',str(SOdata[x + 1]))):
                #This determines if a service is over, that means the other team is serving.
                if (re.search("(?:^|\W)UB(?:$|\W)", serve)):
                    serve = oppname
                else:
                    serve = UBname
            if  (x > 0 and x < lengthOfScores -1)and re.search("(?:^|\W)0-1(?:$|\W)|(?:^|\W)1-0(?:$|\W)",str(scores[x+1])) :
                #every set is different. Therefore there is a need for reinitializing the serve.
                if int(ubscore[x+1]) > 0:
                    serve = UBname
                else:
                    serve = oppname

csvFile.close()
