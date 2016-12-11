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

DROP TABLE IF EXISTS TeamSplits;
DROP TABLE IF EXISTS Conference;
DROP TABLE IF EXISTS Coach;

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


''')

conn.close()

print ('Empty Coach, Conference, and TeamSplits tables have been created')

###############################################################################


#This section creates a list of schools playing in the current school year
#The list is used to generate weblinks which are visited and scraped below
collegesURL = ('http://www.sports-reference.com/cfb/schools/')


if isThisATest.lower() != 'yes':
    try: collegesHTML = urllib.request.urlopen(collegesURL).read()
    except: print ('collegesURL is not working:',collegesURL)
    
    
    colleges = list()
    maxYear = list()
    finalCollegeList = list()
    
    collegesSoup = BeautifulSoup(collegesHTML, 'html.parser')
    collegesTags = collegesSoup('a')
        
    for tag in collegesTags:
        if re.search('.+/cfb/schools/.+', str(tag)):
            collegesString = str(tag.contents)[2:-2]
            collegesString = str(collegesString).lower().strip()
            collegesString = re.sub('\s','-',collegesString)
            collegesString = re.sub('[()]','',collegesString)
            colleges.append(collegesString)  
        else: continue
    
    colleges.pop(0)      
    
    
    collegesTags = collegesSoup('td')
    
    for tag in collegesTags:
        if re.search('data-stat="year_max"',str(tag)):
            maxYearString = (str(tag.contents)[2:-2])
            maxYear.append(maxYearString)
        else: continue
    

    collegesANDmaxYear = zip(colleges, maxYear)
    
    for x, y in collegesANDmaxYear:
        if(int(y) >= int(currentSchoolYear)):
            finalCollegeList.append(x)
        
   
else: finalCollegeList = ['alabama']


print ('Created a list of schools')   

     
########################################################################################

#Defines a function to populate data in the Conference table. The function is called below, after 
# the function to populate the Coach table has also been defined.      
def PushToConference(collegeName, year, conference):
    
        conn = sqlite3.connect('CFBData.db')
        cur = conn.cursor()
    
        cur.execute('''
            INSERT INTO Conference (SchoolName,Year,Conference)
            VALUES (?, ?, ?)''',
            (collegeName, year, conference)
            )
        
        
        conn.commit()
        
        conn.close()
     
#####################################################################################

#Defines a function to populate data in the Coach table. The function is called in the next section.        
def PushToCoach(collegeName, year, coach):
    
        conn = sqlite3.connect('CFBData.db')
        cur = conn.cursor()

        cur.execute('''
            INSERT INTO Coach (SchoolName,Year,Coach)
            VALUES (?, ?, ?)''',
            (collegeName, year, coach)
            )
        
        
        conn.commit()
        
        conn.close()
        
#########################################################################################  
      
#This section iterates through weblinks using the school list above which contain conference and coach data 
#and populates the Conference and Coach data in the database 
print ('Populating Coach and Conference tables. May take several minutes.')

for college in colleges:

    year = thisYear 
    
    conference = ''
    coach = ''
    
    collegeName = str(college)
        
    while year <= currentSchoolYear:
        collegeURLYear = ('http://www.sports-reference.com/cfb/schools/')\
        +college+'/'

        try: 
            collegeStatsYearHTML = urllib.request.urlopen(collegeURLYear).read()
        except: continue
    
        collegeYearSoup = BeautifulSoup(collegeStatsYearHTML, 'html.parser') 
        collegeYearTags = collegeYearSoup('td')
        
        
        for tag in collegeYearTags:
            if re.search(str(year), str(tag.contents)):
                conferenceString = str(tag.contents)
                if re.search('>[A-Za-z].+',conferenceString):
                    conferenceString = re.findall('>[A-Za-z].+',conferenceString)
                    conference = str(conferenceString)[3:-7]
                    PushToConference(collegeName, year, conference)
                    continue
            if re.search('coaches',str(tag)) and re.search(str(year), str(tag)):
                coachString = re.findall('>[A-Z].+?<',str(tag.contents))
                for coaches in coachString:
                    coach = str(coaches)[1:-1]
                    PushToCoach(collegeName, year, coach)
                    
        year = year + 1
        
print ('Conference and Coach tables have been populated')
###############################################################################

#Defines a function to populate data in the TeamSplits table. The function is called in the next section.  
def PushToDB(collegeName,year,side,value,gamesPlayed,wins,losses,offensePassingCompletions\
        ,offensePassingAtmpts,offensePassingCompletePct,offensePassingTotYds\
        ,offensePassingTDs,offenseRushingAtmpts,offenseRushingTotYds,offenseRushingAvgYds\
        ,offenseRushingTDs,totalOffensePlays,totalOffenseTotYds,totalOffenseAvgYds\
        ,firstDownsByPassing,firstDownsByRushing,firstDownsByPenalty,firstDownsTot\
        ,penaltiesTot,penaltiesYds,turnoversByFumble,turnoversByInt,turnoversTot):
        
        conn = sqlite3.connect('CFBData.db')
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
        
        conn.commit()
        
        conn.close()
        
################################################################################

#This section iterates through weblinks using the school list above which contain game data
#and populates the TeamSplits data in the database     
print ('Populating the TeamSplits table. This may take several hours.')
         
for college in colleges:
    
    #print (college)
    collegeName = str(college)
        
    year = thisYear
    
    while year <= currentSchoolYear:
        
        #print (year)

        collegeURL = ('http://www.sports-reference.com/cfb/schools/')\
        +college+'/'+str(year)+'/splits/'
        
        try: collegeStatsHTML = urllib.request.urlopen(collegeURL).read()
        except: 
            year = year + 1
            continue
        
        collegeStatsSoup = BeautifulSoup(collegeStatsHTML, 'html.parser')  
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
                elif x == 1:
                    gamesPlayed = (str(tag.contents)[2:-2])
                elif x == 2:
                    wins = (str(tag.contents)[2:-2])
                elif x == 3:
                    losses = (str(tag.contents)[2:-2])
                elif x == 4:
                    offensePassingCompletions = (str(tag.contents)[2:-2])
                elif x == 5:
                    offensePassingAtmpts = (str(tag.contents)[2:-2])
                elif x == 6:
                    offensePassingCompletePct = (str(tag.contents)[2:-2])
                elif x == 7:
                    offensePassingTotYds = (str(tag.contents)[2:-2])
                elif x == 8:
                    offensePassingTDs = (str(tag.contents)[2:-2])
                elif x == 9:
                    offenseRushingAtmpts = (str(tag.contents)[2:-2])
                elif x == 10:
                    offenseRushingTotYds = (str(tag.contents)[2:-2])
                elif x == 11:
                    offenseRushingAvgYds = (str(tag.contents)[2:-2])
                elif x == 12:
                    offenseRushingTDs = (str(tag.contents)[2:-2])
                elif x == 13:
                    totalOffensePlays = (str(tag.contents)[2:-2])
                elif x == 14:
                    totalOffenseTotYds = (str(tag.contents)[2:-2])
                elif x == 15:
                    totalOffenseAvgYds = (str(tag.contents)[2:-2])
                elif x == 16:
                    firstDownsByPassing = (str(tag.contents)[2:-2])
                elif x == 17:
                    firstDownsByRushing = (str(tag.contents)[2:-2])
                elif x == 18:
                    firstDownsByPenalty = (str(tag.contents)[2:-2])
                elif x == 19:
                    firstDownsTot = (str(tag.contents)[2:-2])
                elif x == 20:
                    penaltiesTot = (str(tag.contents)[2:-2])
                elif x == 21:
                    penaltiesYds = (str(tag.contents)[2:-2])
                elif x == 22:
                    turnoversByFumble = (str(tag.contents)[2:-2])
                elif x == 23:
                    turnoversByInt = (str(tag.contents)[2:-2])
                elif x == 24:
                    turnoversTot = (str(tag.contents)[2:-2])
                    
                x = x + 1 
                    
                if x == 25:
                    PushToDB(collegeName,year,side,value,gamesPlayed,wins,losses,offensePassingCompletions\
                    ,offensePassingAtmpts,offensePassingCompletePct,offensePassingTotYds\
                    ,offensePassingTDs,offenseRushingAtmpts,offenseRushingTotYds,offenseRushingAvgYds\
                    ,offenseRushingTDs,totalOffensePlays,totalOffenseTotYds,totalOffenseAvgYds\
                    ,firstDownsByPassing,firstDownsByRushing,firstDownsByPenalty,firstDownsTot\
                    ,penaltiesTot,penaltiesYds,turnoversByFumble,turnoversByInt,turnoversTot)
                    
                    x = 0
                    run = 0
                    
    
        year = year + 1

print ("Team Splits table has been populated")

print (time.asctime(time.localtime(time.time())))