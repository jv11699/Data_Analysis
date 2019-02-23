'''
The purpose of this file is to be able to easily grab data from the website
 -http://ubbulls.com/sports/wvball/2017-18/files/teamstat.htm- year 2017 UB's volleyball team's statistics
 -http://ubbulls.com/sports/wvball/2018-19/files/teamstat.htm- year 2018 UB's volleyball team's statistics
'''
from bs4 import BeautifulSoup
import re
import urllib.request
import pandas as pd

class Data():
    '''
     A class that grabs the data from the website of the university at buffalo volleyball team  base on the year
     --This link will help in determining the probability very useful: https://prezi.com/tgxlmlfypzwx/math-in-volleyball/
     Probability idea: if errors are not occuring and ub is not on the lead then maybe their probability of scoring next is high
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

        #A main link is preserved base on the year
        if year == 2017:
            url = 'http://ubbulls.com/sports/wvball/2017-18/files/teamstat.htm'
        else:
            url = 'http://ubbulls.com/sports/wvball/2018-19/files/teamstat.htm'
        url_source = urllib.request.urlopen(url).read() #the url request that gets all the url
        self.soup = BeautifulSoup(url_source, 'lxml')  # Conversion to a beautiful soup object
        links = [a for a in (td.find('a', href=True) for td in self.soup.findAll('td')) if a]  # Grabs all the a tags which contains the links
        self.stringLink = []  # Should contain of all the links for the link!
        for link in links:
            if self.year == 2017:
                self.stringLink.append('http://ubbulls.com/sports/wvball/2017-18/files/' + link['href'])  # Each link in the 2017 website is appended inside the StringLink array
            else:
                self.stringLink.append('http://ubbulls.com/sports/wvball/2018-19/files/' + link['href'])  # Each link in the 2018 website is appended inside the StringLink array

    def match(self,match_number, mode='score'):

        #ubscore column opponent score who served that point who the opponent was match number.
        '''
        Scrapes the needed data from the website,
        Modes : 'score' will return both the score of UB and the opponent
                'detail' will return the details for every score
                'data frame' will return a data frame from pandas library
                'name' will return the title of that match

        **Initializations are inside this function to have a better Big-O complexity**

        :param match_number:  the nth number of match, matches are in chronological order where 0 is the latest and the last number is the oldest match
        :param mode: where the mode score will return the scores, and the mode name will return the name of that match
        :return: data dependent on the mode
        '''
        if match_number > len(self.stringLink):
            #if user input is irrational for the parameter: match_number
            raise Exception("The match number excedes the number of matches")

        ######################Initializations###########################################################
        counter = 0 #the counter used to counter the number of titles that will be used in the 'name' mode
        source_scores = urllib.request.urlopen(self.stringLink[match_number]).read()  # the url request that is determined through the match number
        soup_match = BeautifulSoup(source_scores, 'lxml')  # Conversion to a beautiful soup object
        table_html = [table for table in soup_match.find_all('table', {'border':0})] #the table html
        data_frame = pd.read_html(str(table_html)) #this is a panda object that is in a data frame


        ############################################
        #Below are modes that depends on user input#
        ############################################

        #should return the scores of that match
        if mode == 'score':
            scores = [b for b in (td.find('b') for td in soup_match.findAll('td')) if b]  # Grabs all the B tags which contains the scores
            scorePattern = re.findall(r'\d{1,2}-\d{1,2}', self.convBStoString(scores))  # using regular expressions-it finds pattern of [digits - digits]
            return scorePattern

        # returns the details from the game or which team is serving.
        elif mode == 'detail' or  mode == 'SO':
            row_arr= []
            if (mode == 'detail'):
                locationInDataframe = 1
            else:
                locationInDataframe = 2
            if self.year == 2018: #This is added due to different implementation in the html table in the link of 2017 and 2018
                startpos = 7         #On the location in the of the data frame. These numbers are the starting positions of where the information is located
            else:
                startpos = 8
            for i in range(startpos,len(data_frame)): #The range from this for loop is where most of the details are located at from the table
                for index, row in data_frame[i].iterrows(): #It adds the details into an array
                    if (re.search(r'Point',row[1])): #finds row details that have the keyword: Point and appends them to an array
                        row_arr.append(row[locationInDataframe])
            return row_arr
        #should return a data frame object/Panda Object
        elif mode == 'data frame':
            return data_frame

        #should return the name of that match
        elif mode == 'name':
            match_name = [td for td in(self.soup.find_all('td', {'align': 'left'}))]  # list of all the match names of that year
            for i in range(6, len(match_name), 3):  # start: is where the titles start from the html. Iterator: every 3rd because that is where the title is located
                if counter == match_number and mode == 'name': #It would loop through every title till the counter matches the parameter match_number
                  return match_name[i].get_text()
                counter = counter + 1
        elif mode == 'opp name':
            if(re.search(r"Buffalo",data_frame[3][0][1])):
                return data_frame[3][0][3] #these numbers are locations in the data frame that have the names of the teams
            else:                          #They interchange depending on the game, but overall its only these locations that have the teams names
                return data_frame[3][0][1]
        else:
            #if user input is irrational it raises an exception
            raise Exception(r"modes are only 'score' \ 'name' \ 'data frame' \ 'detail' \ 'SO' \ 'stat' \ 'opp name' ")

    def grabTeamScore(self,team, match_number, mode = 'score'):
        '''
        Grabs the score of UB or the opponent's volleyball team during that match
        :param Team: A String parameter that determines if the user wants UB's score or the opponent's score
        :param match_number: A user input that determines the match time
        :param mode: the modes are:  'score' or 'stat' where score will return the scores of a team and stat will return the total stats of the team
        :return: returns an array of scores
        '''
        scoresarr = self.match(match_number)

        #############################################
        # Below are modes that depends on user input#
        #############################################

        #the scores are returned !!
        if mode == 'score':
            detail = self.match(match_number, 'detail')[0]
            #Determines which side of the column is UB's scores or the opponents
            if re.search(r'Point UB', detail) and re.search(r'1-0', scoresarr[0]) \
               or re.search(r'Point UB', detail) is False and re.search(r'0-1', scoresarr[0]):
                    ub_pattern,opp_pattern  = r'\d{1,2}(?=-)', r'(?<=-)\d{1,2}'

            else:                                  #This is added due to the different implementations between websites
                    ub_pattern,opp_pattern = r'(?<=-)\d{1,2}',r'\d{1,2}(?=-)'

            ########USER INPUT##########################################################################################
            if team == 'ub':  # if the parameter is 'ub' then is will return Buffalo scores
                UBscores = re.findall(ub_pattern, str(scoresarr)) #matches strings that have a pattern of: [digits -]
                return UBscores #will return all does matches
            elif team == 'opponent':  # if the parameter is 'opponent' then it will return opponent scores
                OPPscores = re.findall(opp_pattern, str(scoresarr)) #matches strings that have a pattern of: [- digits]
                return OPPscores  #will return all does matches

        #the statistics of each player are returned
        elif mode == 'stat':
            data_frame = self.match(match_number, 'data frame')
            if re.search(r'Buffalo', data_frame[1].iloc[0][1]):
                buff,opp = 1,4
            else:#This is added because in every match buffalo could be in table location 4 or 1 within the data frame
                buff,opp = 4,1

            if team == 'opponent': #Depending on user input, table_loc would reference which team the user needs.
                table_loc = opp
            elif team == 'ub':
                table_loc = buff
            #########################################################################
            for i in range(0, len(data_frame[table_loc])):
                if re.search('Totals',str(data_frame[table_loc].iloc[i])): #Searches for a table that has the keyword: 'Totals"
                    loc = i
            dict = {'SP': data_frame[table_loc].iloc[loc][2], #A dictionary that has the statics of the team
                    'K': data_frame[table_loc].iloc[loc][3],
                    'E': data_frame[table_loc].iloc[loc][4],
                    'TA': data_frame[table_loc].iloc[loc][5],
                    'PCT': data_frame[table_loc].iloc[loc][6],
                    'A': data_frame[table_loc].iloc[loc][7],
                    'SA': data_frame[table_loc].iloc[loc][8],   #The dictionary that contains the
                    'SE': data_frame[table_loc].iloc[loc][9],   #stats for the (SP|K|E|TA|PCT|A|SA|SE|RE|DIGS|BS|BA|BE|BHE)
                    'RE': data_frame[table_loc].iloc[loc][10],
                    'DIGS': data_frame[table_loc].iloc[loc][11],
                    'BS': data_frame[table_loc].iloc[loc][12],
                    'BA': data_frame[table_loc].iloc[loc][13],
                    'BE': data_frame[table_loc].iloc[loc][14],
                    'BHE': data_frame[table_loc].iloc[loc][15]}
            return dict


    def convBStoString(self,bs_objectArr):
        '''
        Converts Array of Beautiful soup objects into a String
        :param bs_objectArr: An array of beautiful soup objects
        :return: It will convert the parameter into a String object
        '''
        texts = ''  # the texts that gets accumulated
        for i in bs_objectArr:
            texts = texts + i.get_text() + "\n"
        return texts

    def numOfMatches(self):
        '''
        :return: returns the number of matches during that year
        '''
        return len(self.stringLink)
#Output Testing
#
UBVolleyball = Data(2018)
#print (Data(2018).match(28)) --> another way to do this
#print(UBVolleyball.match(match_number = 4, mode = 'num matches'), sep="\n")
print(UBVolleyball.numOfMatches())
#print( UBVolleyball.grabTeamScore(team = 'opponent',match_number = 7,mode = 'score'), sep="\n")
