from bs4 import BeautifulSoup
import re
import urllib.request
#THIS IS A BETA VERSION AND wiLL BE USED AS A TEMPLATE FOR FUTHER LINKS
#Using regular expressions
def grabTeamScoreRE(array):
    texts = ''
    for i in array:
        texts = texts + i.get_text() + "\n"
    scores =  re.findall(r'\d{1,2}-\d{1,2}', texts)
    new_String_scores = ''
    for score in scores:
        new_String_scores = new_String_scores + score + "\n"
    return new_String_scores #returns a string conversion of all the scores

#Prints out the list in and converts to text
def print_listInOrder(x, starting_pos):
    for i in range(starting_pos, len(x)):
        print(x[i].get_text())

#Function for grabbing the teams score
def grabTeamScore(Team, array):
    scoresarr= grabTeamScoreRE(array)
    if Team == 'b': #if the parameter is B then is will return Buffalo scores
        UBscores = re.findall(r'\d{1,2}(?=-)', scoresarr)
        for score in UBscores:
            print (score)
    elif Team == 'm': #if the parameter is M then it will return Michigan scores
        OPPscores = re.findall(r'(?<=-)\d{1,2}', scoresarr)
        for score in OPPscores:
            print(score)

#This function I hope will let us figure the emotional factor that comes in to play with UB's volleyball team
def delta_scores():
    global scores
    delta = [] #the disparity among the scores is to be returned
    ub_scores = grabTeamScore('b', scores)
    michigan_scores = grabTeamScore('m',scores)
    for x in range(0, len(ub_scores)):
        delta.append( int(ub_scores[x]) - int(michigan_scores[x]))  #It appends inside the delta array
    return delta

#****************************************************************************************************************************

source = urllib.request.urlopen('http://ubbulls.com/sports/wvball/2017-18/files/ubvb28.htm').read() #the url request
soup = BeautifulSoup(source, 'lxml') #Conversion to a beautiful soup object

#Basically what this does is it grabs all b tags nested inside td and checks if there is <b>, if it has an element inside
scores =[b for b in (td.find('b') for td in soup.findAll('td')) if b] #Grabs all the B tags which contains the scores
allDetail = [tr for tr in soup.findAll('tr') ] #Grabs all the <tr> Tags

user = input("MODE:")
while user != "quit":
    if user == 'ub':
        print(grabTeamScore('b', scores), sep=' ')  # Prints out the team scores depending on whether 'b' for buffalo's team or 'm' for michigan's team
    elif user == 'opp':
        print(grabTeamScore('m', scores), sep=' ')  # Prints out the team scores depending on whether 'b' for buffalo's team or 'm' for michigan's team
    elif user == 'allscore':
       print(grabTeamScoreRE(scores))
    user = input("MODE:")




#print(grabTeamScoreRE(scores))
#These are print outs to test wheter it works or not
print("this is the delta between UB and michigan")
#print(*delta_scores(), sep= ',')
#print_listInOrder(scores,82) #Prints out all the scores
#print_listInOrder(allDetail, 59) #Prints out all the details








