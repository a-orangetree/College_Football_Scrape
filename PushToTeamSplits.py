import urllib.request
from bs4 import BeautifulSoup
import sqlite3
import re
import time

print (time.asctime(time.localtime(time.time())))

isThisATest = 'no'

thisYear = 2006

conn = sqlite3.connect('BettingData.db')
cur = conn.cursor()

cur.executescript('''

DROP TABLE IF EXISTS TeamSplits;
--DROP TABLE IF EXISTS Conference;
--DROP TABLE IF EXISTS Coach;

CREATE TABLE TeamSplits (
    SchoolName TEXT
    ,Year INTEGER
    ,Side TEXT
    ,Value TEXT
    ,GamesPlayed INTEGER
    ,Wins INTEGER
    ,Losses INTEGER
    ,PassCompletions REAL
    ,PassAtmpts REAL
    ,PassCompletionPct REAL
    ,TotalPassYds REAL
    ,PassTDs REAL
    ,RushAtmpts REAL
    ,TotalRushYds REAL
    ,AvgYdsPerRush REAL
    ,RushTDs REAL
    ,TotalPlays REAL
    ,TotalYds REAL
    ,AvgYdsPerPlay REAL
    ,FirstDownsByPass REAL
    ,FirstDownsByRush REAL
    ,FirstDownsByPenalty REAL
    ,TotalFirstDowns REAL
    ,PenaltiesNumber REAL
    ,PenaltiesYds REAL
    ,TurnoversByFumble REAL
    ,TurnoversByInt REAL
    ,TotalTurnovers REAL
);

/*
CREATE TABLE Conference (
    SchoolName TEXT
    ,Year INTEGER
    ,Conference TEXT
);

CREATE TABLE Coach (
    SchoolName TEXT
    ,Year INTEGER
    ,Coach TEXT
);
*/

''')

conn.close()

###############################################################################

collegesURL = ('http://www.sports-reference.com/cfb/schools/')

if isThisATest != 'yes':
    try: collegesHTML = urllib.request.urlopen(collegesURL).read()
    except: print ('collegesURL is not working:',collegesURL)
    
    collegesSoup = BeautifulSoup(collegesHTML, 'html.parser')
    collegesTags = collegesSoup('td')
    
    colleges = list()
    
    for tag in collegesTags:
        if re.search('.+/cfb/schools/.+', str(tag)):
            collegesString = re.findall('>.+',str(tag.contents))
            collegesString = str(collegesString)[3:-7]
            collegesString = str(collegesString).lower().strip()
            collegesString = re.sub('\s','-',collegesString)
            collegesString = re.sub('[()]','',collegesString)
            collegesString = re.sub('&amp;','',collegesString)
        if re.search('2015', str(tag)):
            colleges.append(collegesString)
    #        print (collegesString)
        else: continue
    
#    print (colleges) 

else: colleges = ['air-force']

print ('Done with Schools')

        
########################################################################################
        
#def PushToConference(collegeName, year, conference):
#    
#        conn = sqlite3.connect('BettingData.db')
#        cur = conn.cursor()
#    
#        cur.execute('''
#            INSERT INTO Conference (SchoolName,Year,Conference)
#            VALUES (?, ?, ?)''',
#            (collegeName, year, conference)
#            )
#        
#        
#        conn.commit()
#        
#        conn.close()
     
#####################################################################################
#        
#def PushToCoach(collegeName, year, coach):
#    
#        conn = sqlite3.connect('BettingData.db')
#        cur = conn.cursor()
#
#        cur.execute('''
#            INSERT INTO Coach (SchoolName,Year,Coach)
#            VALUES (?, ?, ?)''',
#            (collegeName, year, coach)
#            )
#        
#        
#        conn.commit()
#        
#        conn.close()
        
#########################################################################################        
    
#for college in colleges:
#
#    year = thisYear 
#    
#    conference = ''
#    coach = ''
#    
#    collegeName = str(college)
#        
#    while year <= 2015:
#        collegeURLYear = ('http://www.sports-reference.com/cfb/schools/')\
#        +college+'/'
#
#        try: 
#            collegeStatsYearHTML = urllib.request.urlopen(collegeURLYear).read()
#        except: continue
#    
#        collegeYearSoup = BeautifulSoup(collegeStatsYearHTML, 'html.parser')
#    #    collegeStatsTags = collegeStatsSoup('table', id='team')  
#        collegeYearTags = collegeYearSoup('td')
#        
#        
#        for tag in collegeYearTags:
##            print (tag)
#            if re.search(str(year), str(tag.contents)):
#                conferenceString = str(tag.contents)
#                if re.search('>[A-Za-z].+',conferenceString):
#                    conferenceString = re.findall('>[A-Za-z].+',conferenceString)
#                    conference = str(conferenceString)[3:-7]
#                    PushToConference(collegeName, year, conference)
#                    continue
##                    print (conference)
#            if re.search('coaches',str(tag)) and re.search(str(year), str(tag)):
#                coachString = re.findall('>[A-Z].+?<',str(tag.contents))
##                print ('1',coachString)
#                for coaches in coachString:
#                    coach = str(coaches)[1:-1]
##                    print ('2',coach)
#                    PushToCoach(collegeName, year, coach)
#                    
#        year = year + 1
#        
#print ('Done with Conferences & Coaches')

###############################################################################

def PushToDB(collegeName,year,side,value,gamesPlayed,wins,losses,offensePassingCompletions\
        ,offensePassingAtmpts,offensePassingCompletePct,offensePassingTotYds\
        ,offensePassingTDs,offenseRushingAtmpts,offenseRushingTotYds,offenseRushingAvgYds\
        ,offenseRushingTDs,totalOffensePlays,totalOffenseTotYds,totalOffenseAvgYds\
        ,firstDownsByPassing,firstDownsByRushing,firstDownsByPenalty,firstDownsTot\
        ,penaltiesTot,penaltiesYds,turnoversByFumble,turnoversByInt,turnoversTot):
        
        conn = sqlite3.connect('BettingData.db')
        cur = conn.cursor()
    
        cur.execute('''
            INSERT INTO TeamSplits (SchoolName, Year, Side, Value, GamesPlayed, Wins
            ,Losses, PassCompletions, PassAtmpts, PassCompletionPct, TotalPassYds
            ,PassTDs, RushAtmpts, TotalRushYds, AvgYdsPerRush, RushTDs, TotalPlays
            ,TotalYds, AvgYdsPerPlay, FirstDownsByPass, FirstDownsByRush, FirstDownsByPenalty
            ,TotalFirstDowns, PenaltiesNumber, PenaltiesYds, TurnoversByFumble, TurnoversByInt
            ,TotalTurnovers)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (collegeName,year,side,value,gamesPlayed,wins,losses,offensePassingCompletions\
            ,offensePassingAtmpts,offensePassingCompletePct,offensePassingTotYds\
            ,offensePassingTDs,offenseRushingAtmpts,offenseRushingTotYds,offenseRushingAvgYds\
            ,offenseRushingTDs,totalOffensePlays,totalOffenseTotYds,totalOffenseAvgYds\
            ,firstDownsByPassing,firstDownsByRushing,firstDownsByPenalty,firstDownsTot\
            ,penaltiesTot,penaltiesYds,turnoversByFumble,turnoversByInt,turnoversTot)
            )
        
#        print ('written')
        
        conn.commit()
        
        conn.close()
        
################################################################################
              
for college in colleges:
    
    print (college)
    collegeName = str(college)
        
    year = thisYear
    
    while year <= 2015:
        
        print (year)

        collegeURL = ('http://www.sports-reference.com/cfb/schools/')\
        +college+'/'+str(year)+'/splits/'
        
        try: collegeStatsHTML = urllib.request.urlopen(collegeURL).read()
        except: continue
        
        collegeStatsSoup = BeautifulSoup(collegeStatsHTML, 'html.parser')
    #    collegeStatsTags = collegeStatsSoup('table', id='team')  
        collegeStatsTags = collegeStatsSoup('td')  

        placeFlag = ''        
        resultFlag = ''
        side = 'Offense'
        value = ''
        gamesPlayed = ''
        wins = ''
        losses = ''
        offensePassingCompletions = ''
        offensePassingAtmpts = ''
        offensePassingCompletePct = ''
        offensePassingTotYds = ''
        offensePassingTDs = ''
        offenseRushingAtmpts = ''
        offenseRushingTotYds = ''
        offenseRushingAvgYds = ''
        offenseRushingTDs = ''
        totalOffensePlays = ''
        totalOffenseTotYds = ''
        totalOffenseAvgYds = ''
        firstDownsByPassing = ''
        firstDownsByRushing = ''
        firstDownsByPenalty = ''
        firstDownsTot = ''
        penaltiesTot = ''
        penaltiesYds = ''
        turnoversByFumble = ''
        turnoversByInt = ''
        turnoversTot = ''    
        
        x = 0
        run = 0
        
        win = ''
        loss = ''
        home = ''
        road = ''
        neutral = ''
        september = ''
        
        for tag in collegeStatsTags:
           
            if ((str(tag.contents)[2:-2] == 'Win') or (str(tag.contents)[2:-2] == 'Loss')\
            or (str(tag.contents)[2:-2] == 'Neutral') or (str(tag.contents)[2:-2] == 'Home')\
            or (str(tag.contents)[2:-2] == 'Road')) or (str(tag.contents)[2:-2] == 'September'):
                
                run = 1
                
                if str(tag.contents)[2:-2] == 'Win':
                    win = 1
                elif str(tag.contents)[2:-2] == 'Loss':
                    loss = 1
                elif str(tag.contents)[2:-2] == 'Home':
                    home = 1
                elif str(tag.contents)[2:-2] == 'Road':
                    road = 1
                elif str(tag.contents)[2:-2] == 'Neutral':
                    neutral = 1
                elif str(tag.contents)[2:-2] == 'September':
                    september = 1
                    run = 0
                    side = 'Defense'
                
            if run == 1:
                if x == 0:
                    value = (str(tag.contents)[2:-2])
#                    print (str(tag.contents)[2:-2])
                elif x == 1:
                    gamesPlayed = (str(tag.contents)[2:-2])
#                    print (str(tag.contents)[2:-2])
                elif x == 2:
                    wins = (str(tag.contents)[2:-2])
#                    print (str(tag.contents)[2:-2])
                elif x == 3:
                    losses = (str(tag.contents)[2:-2])
#                    print (str(tag.contents)[2:-2])
                elif x == 4:
                    offensePassingCompletions = (str(tag.contents)[2:-2])
#                    print (str(tag.contents)[2:-2])
                elif x == 5:
                    offensePassingAtmpts = (str(tag.contents)[2:-2])
#                    print (str(tag.contents)[2:-2])
                elif x == 6:
                    offensePassingCompletePct = (str(tag.contents)[2:-2])
#                    print (str(tag.contents)[2:-2])
                elif x == 7:
                    offensePassingTotYds = (str(tag.contents)[2:-2])
#                    print (str(tag.contents)[2:-2])
                elif x == 8:
                    offensePassingTDs = (str(tag.contents)[2:-2])
#                    print (str(tag.contents)[2:-2])
                elif x == 9:
                    offenseRushingAtmpts = (str(tag.contents)[2:-2])
#                    print (str(tag.contents)[2:-2])
                elif x == 10:
                    offenseRushingTotYds = (str(tag.contents)[2:-2])
#                    print (str(tag.contents)[2:-2])
                elif x == 11:
                    offenseRushingAvgYds = (str(tag.contents)[2:-2])
#                    print (str(tag.contents)[2:-2])
                elif x == 12:
                    offenseRushingTDs = (str(tag.contents)[2:-2])
#                    print (str(tag.contents)[2:-2])
                elif x == 13:
                    totalOffensePlays = (str(tag.contents)[2:-2])
#                    print (str(tag.contents)[2:-2])
                elif x == 14:
                    totalOffenseTotYds = (str(tag.contents)[2:-2])
#                    print (str(tag.contents)[2:-2])
                elif x == 15:
                    totalOffenseAvgYds = (str(tag.contents)[2:-2])
#                    print (str(tag.contents)[2:-2])
                elif x == 16:
                    firstDownsByPassing = (str(tag.contents)[2:-2])
#                    print (str(tag.contents)[2:-2])
                elif x == 17:
                    firstDownsByRushing = (str(tag.contents)[2:-2])
#                    print (str(tag.contents)[2:-2])
                elif x == 18:
                    firstDownsByPenalty = (str(tag.contents)[2:-2])
#                    print (str(tag.contents)[2:-2])
                elif x == 19:
                    firstDownsTot = (str(tag.contents)[2:-2])
#                    print (str(tag.contents)[2:-2])
                elif x == 20:
                    penaltiesTot = (str(tag.contents)[2:-2])
#                    print (str(tag.contents)[2:-2])
                elif x == 21:
                    penaltiesYds = (str(tag.contents)[2:-2])
#                    print (str(tag.contents)[2:-2])
                elif x == 22:
                    turnoversByFumble = (str(tag.contents)[2:-2])
#                    print (str(tag.contents)[2:-2])
                elif x == 23:
                    turnoversByInt = (str(tag.contents)[2:-2])
#                    print (str(tag.contents)[2:-2])
                elif x == 24:
                    turnoversTot = (str(tag.contents)[2:-2])
#                    print (str(tag.contents)[2:-2])
                    
                x = x + 1 
#                print ('X:',x)
                    
                if x == 25:
                    PushToDB(collegeName,year,side,value,gamesPlayed,wins,losses,offensePassingCompletions\
                    ,offensePassingAtmpts,offensePassingCompletePct,offensePassingTotYds\
                    ,offensePassingTDs,offenseRushingAtmpts,offenseRushingTotYds,offenseRushingAvgYds\
                    ,offenseRushingTDs,totalOffensePlays,totalOffenseTotYds,totalOffenseAvgYds\
                    ,firstDownsByPassing,firstDownsByRushing,firstDownsByPenalty,firstDownsTot\
                    ,penaltiesTot,penaltiesYds,turnoversByFumble,turnoversByInt,turnoversTot)
                    
                    x = 0
                    run = 0
                    
#                    if ((win == 1) and (loss == 1) and (home == 1) and (road == 1) and (neutral == ''))\
#                    or ((win == 1) and (loss == 1) and (home == 1) and (road == 1) and (neutral == 1)):
#                        side = 'Defense'
    
        year = year + 1

# print ("Committed to database")

print (time.asctime(time.localtime(time.time())))