from bs4 import BeautifulSoup
import re
import urllib.request


def grabScore(array):
    texts = ''
    for i in array:
        texts = texts + i.get_text() + "\n"
    scores =  re.findall(r'\d{1,2}-\d{1,2}', texts)
    new_String_scores = ''
    for score in scores:
        new_String_scores = new_String_scores + score + "\n"
    return new_String_scores #returns a string conversion of all the scores

#User will have to enter number ranging from 0-27 in chronological order to get the links in chronological order
#Returns string of scores per match
def match(match_number):
    global StringLink
    source = urllib.request.urlopen(StringLink[match_number]).read()  # the url request
    soup = BeautifulSoup(source, 'lxml')  # Conversion to a beautiful soup object
    scores = [b for b in (td.find('b') for td in soup.findAll('td')) if  b]  # Grabs all the B tags which contains the scores
    return grabScore(scores)


'''

'''
def grabTeamScore(Team, match_number):
    scoresarr= match(match_number)
    if Team == 'ub': #if the parameter is B then is will return Buffalo scores
        UBscores = re.findall(r'\d{1,2}(?=-)', scoresarr)
        for score in UBscores:
            print (score)
    elif Team == 'opponent': #if the parameter is M then it will return Michigan scores
        OPPscores = re.findall(r'(?<=-)\d{1,2}', scoresarr)
        for score in OPPscores:
            print(score)

#**********************************************************************************************************************************


source = urllib.request.urlopen('http://ubbulls.com/sports/wvball/2017-18/files/teamstat.htm').read() #the url request
soup = BeautifulSoup(source, 'lxml') #Conversion to a beautiful soup object

links =[a for a in (td.find('a' , href = True) for td in soup.findAll('td')) if a] #Grabs all the a tags which contains the links
counter = 0
StringLink = [] #Should contain of all the links for 2017!
for link in links:
    StringLink.append( 'http://ubbulls.com/sports/wvball/2017-18/files/' + link['href']) #Each link is appended inside the StringLink array

#******************************************************************************************************
'''
THIS IS USER INPUT SO HANDLING THE DATA BECOMES MUCH EASIER
-Basically mode has a choice to see which data to see wheter its UB or the opponent's data 
-the match number input is to see which match it was
- Maybe put this in a dictionary if you grabbed the data's  -voltaire 
'''
user,match_num = input("MODE(ub/opp/allscore/quit):"),input("MATCH NUMBER(0-27):")

while user != "quit":
    if user == 'ub':
        print(grabTeamScore(Team = 'ub', match_number= int(match_num)), sep=' ')  # Prints out the team scores depending on whether 'b' for buffalo's team or 'm' for michigan's team
    elif user == 'opp':
        print(grabTeamScore(Team = 'opponent', match_number= int(match_num)), sep=' ')  # Prints out the team scores depending on whether 'b' for buffalo's team or 'm' for michigan's team
    elif user == 'allscore':
       print(match(match_num))
    user, match_num = input("MODE(ub/opp/allscore):"), input("MATCH NUMBER(0-27):")