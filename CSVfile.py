import DataUBVB as Data
import csv
import re
#The Titles of the CSV file

serviceUB = "UB"
with open('DataofUB','w') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(["UB's score","Opponents Score","Who served that point","Opponent name","Match Number"])
    for i in range(0,Data.numOfMatches()):
        lengthOfScores = len(Data.match(match_number=i, mode='score'))
        ubscore = Data.grabTeamScore(team='ub', match_number=i, mode='score')[0]
        serviceopp =  Data.match(i, 'opp name')
        if (int(ubscore) > 0):
            serve = serviceUB
        else:
            serve = serviceopp
        for x in range(0,lengthOfScores):

            writer.writerow([Data.grabTeamScore(team = 'ub',match_number = i,mode = 'score')[x],
                            Data.grabTeamScore(team = 'opponent', match_number = i, mode = 'score')[x],
                            serve,
                            Data.match(i, 'opp name'),
                            i])
            if (x < lengthOfScores - 1 and re.search(r'so',str(Data.match(i, 'SO')[x + 1]))):
                if (re.search(r'UB', serve)):
                    serve = serviceopp
                else:
                    serve = serviceUB
            if re.search(r'0-1|1-0',Data.match(match_number=i,mode='score')[x]):
                if int(Data.grabTeamScore(team='ub', match_number=i, mode='score')[x]) > 0:
                    serve = serviceUB
                else:
                    serve = serviceopp

csvFile.close()
