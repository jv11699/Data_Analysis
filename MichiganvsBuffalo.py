from bs4 import BeautifulSoup
import urllib.request


#Prints out the list in and converts to text
def print_listInOrder(x, starting_pos):
    for i in range(starting_pos, len(x)):
        print(x[i].get_text())
#Function for grabbing the teams score
def grabTeamScore(Team, array):
    scoresarr= []
    if Team == 'b':
        for i in range(82, len(array)):
            Number = array[i].get_text()
            con_word = str(Number)
            if (con_word[0].isdigit() is True and con_word[0:2].isdigit() is True):
                char = con_word[0:2]
            else:
                char = con_word[0]
            if char.isdigit() is True:
                scoresarr.append(char)
    elif Team == 'm':
        for x in range(82, len(array)):
            Number = array[x].get_text()
            con_word = str(Number)
            for character in range(0,len(con_word)):
                if con_word[character] == '-':
                    char = con_word[1+ character:]
            if con_word[0].isdigit() is True:
                scoresarr.append(char)
    return scoresarr
#This function I hope will let us figure the emotional factor that comes in to play with UB's volleyball team
def delta_scores():
    global scores
    delta = []
    ub_scores = grabTeamScore('b', scores)
    michigan_scores = grabTeamScore('m',scores)
    for x in range(0, len(ub_scores)):
        delta.append( int(ub_scores[x]) - int(michigan_scores[x]))
    return delta



source = urllib.request.urlopen('http://ubbulls.com/sports/wvball/2017-18/files/ubvb28.htm').read()
soup = BeautifulSoup(source, 'lxml')

#Basically what this does is it grabs all b tags nested inside td and checks if there is <b>, if it has an element inside
scores =[b for b in (td.find('b') for td in soup.findAll('td')) if b] #Grabs all the B tags which contains the scores

allDetail = [tr for tr in soup.findAll('tr') ] #Grabs all the <tr> Tags

word = str(scores[120].get_text())

print (scores[90] == u'')
print (word[2] == '-')
print (word[2])

#print (*grabTeamScore('m',scores), sep= ' ') #Prints out the team scores depending on whether 'b' for buffalo's team or 'm' for michigan's team

print("this is the delta between UB and michigan")
print(*delta_scores(), sep= ',')
#print_listInOrder(scores,82) #Prints out all the scores
#print_listInOrder(allDetail, 59) #Prints out all the details



"""
print(soup.title.text)
print (soup.p)                THIS IS TESTING TO SEE WHETER BEAUTIFUL SOUP WORKS 
soup.encode('utf-8')
print(soup.find_all("p")) """





