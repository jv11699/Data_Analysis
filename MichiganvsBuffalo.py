from bs4 import BeautifulSoup
import urllib.request
import io

# from Tools.scripts.parse_html5_entities import fname
source = urllib.request.urlopen('https://pythonprogramming.net/parsememcparseface/').read()
x = 12
soup = BeautifulSoup(source, 'html.parser')

print(soup.find_all('p'))
"""
print(soup.title.text)
print (soup.p)                THIS IS TESTING TO SEE WHETER BEAUTIFUL SOUP WORKS 
soup.encode('utf-8')
print(soup.find_all("p")) """





