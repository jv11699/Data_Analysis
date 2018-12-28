from bs4 import BeautifulSoup
import re
import urllib.request

#Using regular expressions
def grabTeamScoreRE():
    
#Prints out the list in and converts to text
def print_listInOrder(x, starting_pos):
    for i in range(starting_pos, len(x)):
        print(x[i].get_text())
#Function for grabbing the teams score
def grabTeamScore(Team, array):
    scoresarr= [] #the array which will hold the scores
    if Team == 'b': #if the parameter is B then is will return Buffalo scores
        for i in range(82, len(array)): #uses subtring string methods to scrape scofes
            Number = array[i].get_text()
            con_word = str(Number)
            if (con_word[0].isdigit() is True and con_word[0:2].isdigit() is True):
                char = con_word[0:2]
            else:
                char = con_word[0]
            if char.isdigit() is True:
                scoresarr.append(char)
    elif Team == 'm': #if the parameter is M then it will return Michigan scores
        for x in range(82, len(array)): #The array starts at 82 Because according to the html thats where the scores start
            Number = array[x].get_text()
            con_word = str(Number)
            for character in range(0,len(con_word)):
                if con_word[character] == '-': #it finds the seperation
                    char = con_word[1+ character:]
            if con_word[0].isdigit() is True:
                scoresarr.append(char)
    return scoresarr
#This function I hope will let us figure the emotional factor that comes in to play with UB's volleyball team
def delta_scores():
    global scores
    delta = [] #the disparity among the scores is to be returned
    ub_scores = grabTeamScore('b', scores)
    michigan_scores = grabTeamScore('m',scores)
    for x in range(0, len(ub_scores)):
        delta.append( int(ub_scores[x]) - int(michigan_scores[x]))  #It appends inside the delta array
    return delta



source = urllib.request.urlopen('http://ubbulls.com/sports/wvball/2017-18/files/ubvb28.htm').read() #the url request
soup = BeautifulSoup(source, 'lxml') #Conversion to a beautiful soup object 

#Basically what this does is it grabs all b tags nested inside td and checks if there is <b>, if it has an element inside
scores =[b for b in (td.find('b') for td in soup.findAll('td')) if b] #Grabs all the B tags which contains the scores

allDetail = [tr for tr in soup.findAll('tr') ] #Grabs all the <tr> Tags

word = str(scores[120].get_text())

print (scores[90] == u'')
print (word[2] == '-')
print (word[2])

#These are print outs to test wheter it works or not
print (*grabTeamScore('m',scores), sep= ' ') #Prints out the team scores depending on whether 'b' for buffalo's team or 'm' for michigan's team

print("this is the delta between UB and michigan")
#print(*delta_scores(), sep= ',')
#print_listInOrder(scores,82) #Prints out all the scores
#print_listInOrder(allDetail, 59) #Prints out all the details








