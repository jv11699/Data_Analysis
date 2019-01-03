from bs4 import BeautifulSoup
import re
import urllib.request
#import pandas 
class Data():
    '''
     A class that grabs the data of the volleyball of the university at buffalo team  base on the year
     --This link will help in determining the probability very useful: https://prezi.com/tgxlmlfypzwx/math-in-volleyball/
     Probability idea: if errors are not occuring and ub is not on the lead then maybe their probability of scoring next is high
     **** Use this as a library to grab data easily ***
        ...
        Attributes
        - - - - - -
        year:  the Year of the matches
        url: the url of the matches during that year
        soup: the beautiful soup object which grabs the html format of the url
        stringLink: an array that contains all of the individual matches' url link during that year
    '''
    def __init__(self, year):
        '''
        :param year: The year of the data UB's volley ball team played
        '''
        if year != 2017 and year != 2018:
            raise Exception("The years are only from 2017 and 2018")
        self.year = year
        if year == 2017:
            self.__url = 'http://ubbulls.com/sports/wvball/2017-18/files/teamstat.htm'
        else:
            self.__url = 'http://ubbulls.com/sports/wvball/2018-19/files/teamstat.htm'
        url_source = urllib.request.urlopen(self.__url).read() #the url request that gets all the url
        self.soup = BeautifulSoup(url_source, 'lxml')  # Conversion to a beautiful soup object
        links = [a for a in (td.find('a', href=True) for td in self.soup.findAll('td')) if a]  # Grabs all the a tags which contains the links
        self.stringLink = []  # Should contain of all the links for the link!
        for link in links:
            if self.year == 2017:
                self.stringLink.append('http://ubbulls.com/sports/wvball/2017-18/files/' + link['href'])  # Each link is appended inside the StringLink array
            else:
                self.stringLink.append('http://ubbulls.com/sports/wvball/2018-19/files/' + link['href'])  # Each link is appended inside the StringLink array

    def grabScore(self,array):
        '''
        This function grabs all of the score from the match

        :param array: an array of the beautiful soup which should contain all of the scores
        :return: returns an array of the scores if the mode is set on score, and an array of
        '''

        scores = re.findall(r'\d{1,2}-\d{1,2}', self.convBStoString(array))  # using regular expressions
        score_arr = []
        for score in scores:  # since regular expression returns a list of all found patterns
            score_arr.append(score)
        return score_arr  # returns a string conversion of all the scores

    def match(self,match_number, mode='score'):
        '''

        :param match_number:  the nth number of match, matches are in chronological order where 0 is the latest and the last number is the oldest match
        :param mode: where the mode score will return the scores, and the mode name will return the name of that match
        :return: data base off the mode, score: will return scores, name: will return the title of that match
        '''
        if match_number > len(self.stringLink):
            raise Exception("The match number excedes the number of matches")
        counter = 0
        source_scores = urllib.request.urlopen(self.stringLink[match_number]).read()  # the url request
        soup_match = BeautifulSoup(source_scores, 'lxml')  # Conversion to a beautiful soup object
        scores = [b for b in (td.find('b') for td in soup_match.findAll('td')) if b]  # Grabs all the B tags which contains the scores
        match_name = [td for td in (self.soup.find_all('td', {'align':'left'}))]
        details = [table for table in soup_match.find_all('table', {'border':0})]
#NEED WORK ON THIS PART
        detailScore = re.findall(r'(?<=Points)', self.convBStoString(details))
        #should return the scores of that match
        if mode == 'score':
            return  details[7].get_text() #self.grabScore(scores)
        #should return the name of that match
        elif mode == 'name':
            for i in range(6, len(match_name), 3):
                if counter == match_number:
                  return match_name[i].get_text()
                counter = counter + 1
        #Score with details
        else:
            raise Exception("modes are only \'score\'\\'name\'")

    def grabTeamScore(self,Team, match_number):
        scoresarr = self.match(match_number)
        score_arr = []
        if Team == 'ub':  # if the parameter is B then is will return Buffalo scores
            UBscores = re.findall(r'\d{1,2}(?=-)', str(scoresarr))
            for score in UBscores:
                score_arr.append(score)
        elif Team == 'opponent':  # if the parameter is M then it will return Michigan scores
            OPPscores = re.findall(r'(?<=-)\d{1,2}', str(scoresarr))
            for score in OPPscores:
                score_arr.append(score)
        return score_arr


    def convBStoString(self,bs_objectArr):
        texts = ''  # the texts that gets accumulated
        for i in bs_objectArr:
            texts = texts + i.get_text() + "\n"
        return texts
UBVolleyball = Data(2018)
print( UBVolleyball.match(match_number = 3, mode = 'score'))