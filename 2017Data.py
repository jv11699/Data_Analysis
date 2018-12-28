from bs4 import BeautifulSoup
import re
import urllib.request

#Matches are from 0 - 27 since in 2017 there are total of 28 matches
#User will have to enter number ranging from 0-27 in chronological order to get the links in chronological order
def grabLink(Match):
    

#THE GOAL IS ONCE This module is imported then it can just be called and maybe use a dictionary
source = urllib.request.urlopen('http://ubbulls.com/sports/wvball/2017-18/files/teamstat.htm').read() #the url request
soup = BeautifulSoup(source, 'lxml') #Conversion to a beautiful soup object

links =[a for a in (td.find('a' , href = True) for td in soup.findAll('td')) if a] #Grabs all the a tags which contains the links
counter = 0
StringLink = [] #Should contain of all the links for 2017!
for link in links:
    StringLink.append( 'http://ubbulls.com/sports/wvball/2017-18/files/' + link['href'])

for word in StringLink:
    print(word)
