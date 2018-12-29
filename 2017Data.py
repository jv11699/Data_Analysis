from bs4 import BeautifulSoup
import re
import urllib.request

'''
*A function when called upon grabs string that have "[digits] - [digits]" pattern 
    using regular expression 
'''
def grabScore(array):
    texts = '' #the texts that gets accumulated
    for i in array:
        texts = texts + i.get_text() + "\n"
    scores =  re.findall(r'\d{1,2}-\d{1,2}', texts) #using regular expressions
    new_String_scores = ''
    for score in scores: #since regular expression returns a list of all found patterns
        new_String_scores = new_String_scores + score + "\n"
    return new_String_scores #returns a string conversion of all the scores

'''
* A function when called upon will give the matches score or name 
    @param match_number the nth number of match, matches are in chronological order where 0 is the latest and 27 is the oldest match 
    @param mode the mode can either be 'score' or 'name' where score will return the scores of that match and name will return the name of that match  
'''
def match(match_number, mode = 'score'):
    string_names = ''
    global StringLink
    source_scores = urllib.request.urlopen(StringLink[match_number]).read()  # the url request
    main_source = urllib.request.urlopen('http://ubbulls.com/sports/wvball/2017-18/files/teamstat.htm').read()
    soup = BeautifulSoup(source_scores, 'lxml')  # Conversion to a beautiful soup object
    soup2 = BeautifulSoup(main_source, 'lxml')
    scores = [b for b in (td.find('b') for td in soup.findAll('td')) if  b]  # Grabs all the B tags which contains the scores
    match_name = [td for td in (soup2.find_all('td', {'align': 'left'}))]
    if mode == 'score':
        return grabScore(scores)
    elif mode == 'name':
        return string_names[match_number].get_text()


'''
*grabs the specific team score whether its UB or the opposing team 
 @param Team where is team is 'ub' will return UB's score during that match, or 'opponent' where it will return the opponents score on that match 
 @param match_number the nth number of that match 
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


source = urllib.request.urlopen('http://ubbulls.com/sports/wvball/2017-18/files/teamstat.htm').read() #the url request that gets all the url 
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
        match_mode = input("score/name? ")
        if match_mode == 'score':
            print(match(int(match_num)))
        else:
            print(match(int(match_num),'name'))
    user, match_num = input("MODE(ub/opp/allscore):"), input("MATCH NUMBER(0-27):")
