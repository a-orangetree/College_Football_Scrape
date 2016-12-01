import urllib.request
from bs4 import BeautifulSoup
import sqlite3
import re
import time

print (time.asctime(time.localtime(time.time())))

isThisATest = 'no'

thisYear = 2010

conn = sqlite3.connect('BettingData.db')
cur = conn.cursor()

cur.executescript('''

DROP TABLE IF EXISTS TeamStatistics;

CREATE TABLE TeamStatistics (
    SchoolName TEXT
    ,Year TEXT
    ,Side TEXT
    ,GamesPlayed INTEGER
    ,offensePassingCompletions REAL
    ,offensePassingAtmpts REAL
    ,offensePassingCompletePct REAL
    ,offensePassingTotYds REAL
    ,offensePassingTDs REAL
    ,offenseRushingAtmpts REAL
    ,offenseRushingTotYds REAL
    ,offenseRushingAvgYds REAL
    ,offenseRushingTDs REAL
    ,totalOffensePlays REAL
    ,totalOffenseTotYds REAL
    ,totalOffenseAvgYds REAL
    ,firstDownsByPassing REAL
    ,firstDownsByRushing REAL
    ,firstDownsByPenalty REAL
    ,firstDownsTot REAL
    ,penaltiesTot REAL
    ,penaltiesYds REAL
    ,turnoversByFumble REAL
    ,turnoversByInt REAL
    ,turnoversTot REAL

);

''')

collegesURL = ('http://www.sports-reference.com/cfb/schools/')

if isThisATest != 'yes':
    try: collegesHTML = urllib.request.urlopen(collegesURL).read()
    except: print ('collegesURL is not working:',collegesURL)
    
    collegesSoup = BeautifulSoup(collegesHTML, 'html.parser')
    collegesTags = collegesSoup('a')
    
    colleges = list()
    
    for tag in collegesTags:
#        print ('Tag:',tag)
        if re.search('.+/cfb/schools/.+', str(tag)):
            collegesString = str(tag.contents)[2:-2]
            collegesString = str(collegesString).lower().strip()
            collegesString = re.sub('\s','-',collegesString)
            collegesString = re.sub('[()]','',collegesString)
            colleges.append(collegesString)
        else: continue
else: colleges = ['alabama','florida-international']

#print (colleges)

def PushToDB(collegeName,year,side,gamesPlayed,offensePassingCompletions\
        ,offensePassingAtmpts,offensePassingCompletePct,offensePassingTotYds\
        ,offensePassingTDs,offenseRushingAtmpts,offenseRushingTotYds,offenseRushingAvgYds\
        ,offenseRushingTDs,totalOffensePlays,totalOffenseTotYds,totalOffenseAvgYds\
        ,firstDownsByPassing,firstDownsByRushing,firstDownsByPenalty,firstDownsTot\
        ,penaltiesTot,penaltiesYds,turnoversByFumble,turnoversByInt,turnoversTot):
        
        conn = sqlite3.connect('BettingData.db')
        cur = conn.cursor()
    
        cur.execute('''
            INSERT INTO TeamStatistics (SchoolName,year,side,gamesPlayed,offensePassingCompletions
            ,offensePassingAtmpts,offensePassingCompletePct,offensePassingTotYds
            ,offensePassingTDs,offenseRushingAtmpts,offenseRushingTotYds,offenseRushingAvgYds
            ,offenseRushingTDs,totalOffensePlays,totalOffenseTotYds,totalOffenseAvgYds
            ,firstDownsByPassing,firstDownsByRushing,firstDownsByPenalty,firstDownsTot
            ,penaltiesTot,penaltiesYds,turnoversByFumble,turnoversByInt,turnoversTot)
            VALUES (?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (collegeName,year,side,gamesPlayed,offensePassingCompletions\
            ,offensePassingAtmpts,offensePassingCompletePct,offensePassingTotYds\
            ,offensePassingTDs,offenseRushingAtmpts,offenseRushingTotYds,offenseRushingAvgYds\
            ,offenseRushingTDs,totalOffensePlays,totalOffenseTotYds,totalOffenseAvgYds\
            ,firstDownsByPassing,firstDownsByRushing,firstDownsByPenalty,firstDownsTot\
            ,penaltiesTot,penaltiesYds,turnoversByFumble,turnoversByInt,turnoversTot)
            )
        
        conn.commit()

collegesLinks = list()

for college in colleges:
    
    print (college)
    
    year = thisYear
    
    while year <= 2015:
        
        print (year)
        
        collegeName = college    
        
        collegeURL = ('http://www.sports-reference.com/cfb/schools/')\
        +str(college)+'/'+str(year)+'.html'
    
        try: collegeStatsHTML = urllib.request.urlopen(collegeURL).read()
        except: continue
        
        collegeStatsSoup = BeautifulSoup(collegeStatsHTML, 'html.parser')
    #    collegeStatsTags = collegeStatsSoup('table', id='team')  
        collegeStatsTags = collegeStatsSoup('td')  
        
        side = ''
        gamesPlayed = ''
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
        y = 0
        
        for tag in collegeStatsTags:
            if x == 0:
                side = (str(tag.contents)[2:-2])
            elif x == 1:
                gamesPlayed = (str(tag.contents)[2:-2])
            elif x == 2:
                offensePassingCompletions = (str(tag.contents)[2:-2])
            elif x == 3:
                offensePassingAtmpts = (str(tag.contents)[2:-2])
            elif x == 4:
                offensePassingCompletePct = (str(tag.contents)[2:-2])
            elif x == 5:
                offensePassingTotYds = (str(tag.contents)[2:-2])
            elif x == 6:
                offensePassingTDs = (str(tag.contents)[2:-2])
            elif x == 7:
                offenseRushingAtmpts = (str(tag.contents)[2:-2])
            elif x == 8:
                offenseRushingTotYds = (str(tag.contents)[2:-2])
            elif x == 9:
                offenseRushingAvgYds = (str(tag.contents)[2:-2])
            elif x == 10:
                offenseRushingTDs = (str(tag.contents)[2:-2])
            elif x == 11:
                totalOffensePlays = (str(tag.contents)[2:-2])
            elif x == 12:
                totalOffenseTotYds = (str(tag.contents)[2:-2])
            elif x == 13:
                totalOffenseAvgYds = (str(tag.contents)[2:-2])
            elif x == 14:
                firstDownsByPassing = (str(tag.contents)[2:-2])
            elif x == 15:
                firstDownsByRushing = (str(tag.contents)[2:-2])
            elif x == 16:
                firstDownsByPenalty = (str(tag.contents)[2:-2])
            elif x == 17:
                firstDownsTot = (str(tag.contents)[2:-2])
            elif x == 18:
                penaltiesTot = (str(tag.contents)[2:-2])
            elif x == 19:
                penaltiesYds = (str(tag.contents)[2:-2])
            elif x == 20:
                turnoversByFumble = (str(tag.contents)[2:-2])
            elif x == 21:
                turnoversByInt = (str(tag.contents)[2:-2])
            elif x == 22:
                turnoversTot = (str(tag.contents)[2:-2])
                
            x = x + 1
    #        print ('X:',x)
    #        print ('Y:',y)
            
            if x == 23 and y == 1:
    #            print ('1')            
                
                PushToDB(collegeName,year,side,gamesPlayed,offensePassingCompletions\
                    ,offensePassingAtmpts,offensePassingCompletePct,offensePassingTotYds\
                    ,offensePassingTDs,offenseRushingAtmpts,offenseRushingTotYds,offenseRushingAvgYds\
                    ,offenseRushingTDs,totalOffensePlays,totalOffenseTotYds,totalOffenseAvgYds\
                    ,firstDownsByPassing,firstDownsByRushing,firstDownsByPenalty,firstDownsTot\
                    ,penaltiesTot,penaltiesYds,turnoversByFumble,turnoversByInt,turnoversTot)
                continue
            
            if x == 23 and y == 0:
    #            print ('2')            
                
                PushToDB(collegeName,year,side,gamesPlayed,offensePassingCompletions\
                    ,offensePassingAtmpts,offensePassingCompletePct,offensePassingTotYds\
                    ,offensePassingTDs,offenseRushingAtmpts,offenseRushingTotYds,offenseRushingAvgYds\
                    ,offenseRushingTDs,totalOffensePlays,totalOffenseTotYds,totalOffenseAvgYds\
                    ,firstDownsByPassing,firstDownsByRushing,firstDownsByPenalty,firstDownsTot\
                    ,penaltiesTot,penaltiesYds,turnoversByFumble,turnoversByInt,turnoversTot)
                x = 0
                y = 1
         
        year = year + 1

# print ("Committed to database")
print (time.asctime(time.localtime(time.time())))