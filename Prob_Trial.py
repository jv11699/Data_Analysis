'''
Website basis: http://www.righto.com/2011/07/mathematics-of-volleyball.html
This is a beta version of probability testing
*The goal of this file is to be able to see patterns
Events:
    Error
    Kill
Sample Space:
    {UB gaining a score, UB losing a score}


NOTE: SINCE OF THE RALLY POINT SYSTEM PROBABILITY OF SCORING WHEN A TEAM HAS THE BALL IN HAND IS HIGH
Formula? p(m,n) = p(m+1,n)+ p(m,n+1) / 2
'''
from DataUBVB import Data
import re
num_Outcome = 0 #the number of times this occurence occured
dataMatch = Data(2018)
def emotional_outcome(data):
    '''
    this is proof of wheter ub doesnt score when they are on the lead
    :param data:
    :return:
    '''

def errors(data):
    '''
    This calculates areas where ub lost due to its number of errors
    :param data:
    :return:
    '''
