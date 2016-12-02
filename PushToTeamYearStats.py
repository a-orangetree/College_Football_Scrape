import urllib.request
from bs4 import BeautifulSoup
import sqlite3
import re
import time


# currentSchoolYear should be year which the current or last college football season began.
# So, if it is the 2016-2017 season, you would enter 2016.
currentSchoolYear = 2016

# Used for testing. If "Yes" only a subsection of schools will be scraped and populated in the database
isThisATest = 'no'


#########################################################################
# Below creates tables ready to receive data for the Coach, Conference, and Team Splits tables
print (time.asctime(time.localtime(time.time())))
thisYear = (currentSchoolYear - 9)

conn = sqlite3.connect('CFBData.db')
cur = conn.cursor()

cur.executescript('''

DROP TABLE IF EXISTS TeamStatistics;

CREATE TABLE TeamStatistics (
    SchoolName TEXT
    ,Year TEXT
    ,Side TEXT
    ,GamesPlayed INTEGER
    ,PassingCompletions REAL
    ,PassingAtmpts REAL
    ,PassingCompletePct REAL
    ,PassingTotYds REAL
    ,PassingTDs REAL
    ,RushingAtmpts REAL
    ,RushingTotYds REAL
    ,RushingAvgYds REAL
    ,RushingTDs REAL
    ,TotalOffensePlays REAL
    ,TotalOffenseTotYds REAL
    ,TotalOffenseAvgYds REAL
    ,FirstDownsByPassing REAL
    ,FirstDownsByRushing REAL
    ,FirstDownsByPenalty REAL
    ,FirstDownsTot REAL
    ,PenaltiesTot REAL
    ,PenaltiesYds REAL
    ,TurnoversByFumble REAL
    ,TurnoversByInt REAL
    ,TurnoversTot REAL

);

''')

print ('An empty TeamStatistics table has been created')


#########################################################################

#This section creates a list of schools playing in the current school year
#The list is used to generate weblinks which are visited and scraped below
collegesURL = ('http://www.sports-reference.com/cfb/schools/')

if isThisATest != 'yes':
    try: collegesHTML = urllib.request.urlopen(collegesURL).read()
    except: print ('collegesURL is not working:',collegesURL)
    
    collegesSoup = BeautifulSoup(collegesHTML, 'html.parser')
    collegesTags = collegesSoup('a')
    
    colleges = list()
    
    for tag in collegesTags:

        if re.search('.+/cfb/schools/.+', str(tag)):
            collegesString = str(tag.contents)[2:-2]
            collegesString = str(collegesString).lower().strip()
            collegesString = re.sub('\s','-',collegesString)
            collegesString = re.sub('[()]','',collegesString)
            colleges.append(collegesString)
        else: continue
else: colleges = ['alabama','florida-international']


################################################################################

#Defines a function to populate data in the Team Statistics table. The function is called in the next section. 
def PushToDB(collegeName,year,side,gamesPlayed,offensePassingCompletions\
        ,offensePassingAtmpts,offensePassingCompletePct,offensePassingTotYds\
        ,offensePassingTDs,offenseRushingAtmpts,offenseRushingTotYds,offenseRushingAvgYds\
        ,offenseRushingTDs,totalOffensePlays,totalOffenseTotYds,totalOffenseAvgYds\
        ,firstDownsByPassing,firstDownsByRushing,firstDownsByPenalty,firstDownsTot\
        ,penaltiesTot,penaltiesYds,turnoversByFumble,turnoversByInt,turnoversTot):
        
        conn = sqlite3.connect('CFBData.db')
        cur = conn.cursor()
    
        cur.execute('''
            INSERT INTO TeamStatistics (SchoolName,Year,Side,GamesPlayed,PassingCompletions
            ,PassingAtmpts,PassingCompletePct,PassingTotYds
            ,PassingTDs,RushingAtmpts,RushingTotYds,RushingAvgYds
            ,RushingTDs,TotalOffensePlays,TotalOffenseTotYds,TotalOffenseAvgYds
            ,FirstDownsByPassing,FirstDownsByRushing,FirstDownsByPenalty,FirstDownsTot
            ,PenaltiesTot,PenaltiesYds,TurnoversByFumble,TurnoversByInt,TurnoversTot)
            VALUES (?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (collegeName,year,side,gamesPlayed,offensePassingCompletions\
            ,offensePassingAtmpts,offensePassingCompletePct,offensePassingTotYds\
            ,offensePassingTDs,offenseRushingAtmpts,offenseRushingTotYds,offenseRushingAvgYds\
            ,offenseRushingTDs,totalOffensePlays,totalOffenseTotYds,totalOffenseAvgYds\
            ,firstDownsByPassing,firstDownsByRushing,firstDownsByPenalty,firstDownsTot\
            ,penaltiesTot,penaltiesYds,turnoversByFumble,turnoversByInt,turnoversTot)
            )
        
        conn.commit()
        
        
#########################################################################        

#This section iterates through weblinks using the school list above which contain game data
#and populates the TeamSplits data in the database     
print ('Populating the TeamStatistics table. This may take several hours.')
for college in colleges:
    
    year = thisYear
    
    while year <= 2015:
        
        collegeName = college    
        
        collegeURL = ('http://www.sports-reference.com/cfb/schools/')\
        +str(college)+'/'+str(year)+'.html'
    
        try: collegeStatsHTML = urllib.request.urlopen(collegeURL).read()
        except: 
            year = year + 1
            continue
        
        collegeStatsSoup = BeautifulSoup(collegeStatsHTML, 'html.parser')    
        collegeStatsTags = collegeStatsSoup('td')  
        
        side = ''
        gamesPlayed = ''
        PassingCompletions = ''
        PassingAtmpts = ''
        PassingCompletePct = ''
        PassingTotYds = ''
        PassingTDs = ''
        RushingAtmpts = ''
        RushingTotYds = ''
        RushingAvgYds = ''
        RushingTDs = ''
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
                gamesPlayed = (str(tag.contents)[2:-2])
            elif x == 1:
                PassingCompletions = (str(tag.contents)[2:-2])
            elif x == 2:
                PassingAtmpts = (str(tag.contents)[2:-2])
            elif x == 3:
                PassingCompletePct = (str(tag.contents)[2:-2])
            elif x == 4:
                PassingTotYds = (str(tag.contents)[2:-2])
            elif x == 5:
                PassingTDs = (str(tag.contents)[2:-2])
            elif x == 6:
                RushingAtmpts = (str(tag.contents)[2:-2])
            elif x == 7:
                RushingTotYds = (str(tag.contents)[2:-2])
            elif x == 8:
                RushingAvgYds = (str(tag.contents)[2:-2])
            elif x == 9:
                RushingTDs = (str(tag.contents)[2:-2])
            elif x == 10:
                totalOffensePlays = (str(tag.contents)[2:-2])
            elif x == 11:
                totalOffenseTotYds = (str(tag.contents)[2:-2])
            elif x == 12:
                totalOffenseAvgYds = (str(tag.contents)[2:-2])
            elif x == 13:
                firstDownsByPassing = (str(tag.contents)[2:-2])
            elif x == 14:
                firstDownsByRushing = (str(tag.contents)[2:-2])
            elif x == 15:
                firstDownsByPenalty = (str(tag.contents)[2:-2])
            elif x == 16:
                firstDownsTot = (str(tag.contents)[2:-2])
            elif x == 17:
                penaltiesTot = (str(tag.contents)[2:-2])
            elif x == 18:
                penaltiesYds = (str(tag.contents)[2:-2])
            elif x == 19:
                turnoversByFumble = (str(tag.contents)[2:-2])
            elif x == 20:
                turnoversByInt = (str(tag.contents)[2:-2])
            elif x == 21:
                turnoversTot = (str(tag.contents)[2:-2])
                
            x = x + 1
            
            if x == 22 and y == 1:

                side = 'Defense'           
                
                PushToDB(collegeName,year,side,gamesPlayed,PassingCompletions\
                    ,PassingAtmpts,PassingCompletePct,PassingTotYds\
                    ,PassingTDs,RushingAtmpts,RushingTotYds,RushingAvgYds\
                    ,RushingTDs,totalOffensePlays,totalOffenseTotYds,totalOffenseAvgYds\
                    ,firstDownsByPassing,firstDownsByRushing,firstDownsByPenalty,firstDownsTot\
                    ,penaltiesTot,penaltiesYds,turnoversByFumble,turnoversByInt,turnoversTot)
                continue
            
            if x == 22 and y == 0:

                side = 'Offense'           
                
                PushToDB(collegeName,year,side,gamesPlayed,PassingCompletions\
                    ,PassingAtmpts,PassingCompletePct,PassingTotYds\
                    ,PassingTDs,RushingAtmpts,RushingTotYds,RushingAvgYds\
                    ,RushingTDs,totalOffensePlays,totalOffenseTotYds,totalOffenseAvgYds\
                    ,firstDownsByPassing,firstDownsByRushing,firstDownsByPenalty,firstDownsTot\
                    ,penaltiesTot,penaltiesYds,turnoversByFumble,turnoversByInt,turnoversTot)
                x = 0
                y = 1
         
        year = year + 1

print ("TeamStatistics table has been populated")

print (time.asctime(time.localtime(time.time())))
