from bs4 import BeautifulSoup
import urllib.request
import io

# from Tools.scripts.parse_html5_entities import fname
source = urllib.request.urlopen('http://ubbulls.com/sports/wvball/2017-18/files/ubvb28.htm').read()
x = 12
soup = BeautifulSoup(source, 'lxml')
ele = soup('font', face="verdana")
#DRAFT STARTS AT 59
for i in range(59,len(soup.find_all('tr'))):
    print(soup.find_all('tr')[i].get_text())


"""
print(soup.title.text)
print (soup.p)                THIS IS TESTING TO SEE WHETER BEAUTIFUL SOUP WORKS 
soup.encode('utf-8')
print(soup.find_all("p")) """





