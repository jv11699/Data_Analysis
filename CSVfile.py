from DataUBVB import Data
import csv
import re
#The Titles of the CSV file
VolleyBallData = Data(2017)
serviceUB = "service of UB"
with open('DataSciProj','w') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(["UB's score","Opponents Score","Who served that point","Opponent name","Match Number"])
    for i in range(VolleyBallData.numOfMatches()):
        lengthOfMatches = len(VolleyBallData.match(match_number=i, mode='SO'))
        for x in range(lengthOfMatches):
            ubscore = VolleyBallData.grabTeamScore(match_number=i, team='ub')
            serviceopp = "service of " + VolleyBallData.match(i, 'opp name')
            if (x == 0):
                if (ubscore > 0):
                    service = serviceUB
                else:
                    service = serviceopp
            writer.writerow([ubscore,
                            VolleyBallData.grabTeamScore(match_number=i, team='opp'),
                            service,
                            VolleyBallData.match(i, 'opp name'),
                            i])
            if (i < lengthOfMatches - 1 and VolleyBallData.match(i, 'SO')[i + 1] == 'so'):
                if (service == serviceUB):
                    service = serviceopp
                else:
                    service = serviceUB

csvFile.close()
