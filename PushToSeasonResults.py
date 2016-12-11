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
# Below creates tables ready to receive data for the Season Results tables
print (time.asctime(time.localtime(time.time())))
thisYear = currentSchoolYear - 9

conn = sqlite3.connect('CFBData.db')
cur = conn.cursor()

cur.executescript('''

DROP TABLE IF EXISTS SeasonResults;
DROP TABLE IF EXISTS GameResults;

CREATE TABLE SeasonResults (
    SchoolName TEXT
    ,Year INTEGER
    ,GameOfYear INTEGER
    ,Date TEXT
    ,Time TEXT
    ,Day TEXT
    ,HomeOrAway TEXT
    ,Opponent TEXT
    ,Outcome TEXT
    ,PointsFor INTEGER
    ,PointsAgainst INTEGER
    ,Wins INTEGER
    ,Losses INTEGER
    ,Streak TEXT

);

''')

print ('An empty SeasonResults table has been created')

conn.close()

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
###############################################################################


#Defines a function to populate data in the SeasonResults table. The function is called in the next section. 
def PushToSeasonResults(schoolName,year,gameofYear,date,time,day,homeOrAway,opponent,outcome\
    ,pointsFor,pointsAgainst,wins,losses,streak):
        
    conn = sqlite3.connect('CFBData.db')
    cur = conn.cursor()

    cur.execute('''
        INSERT INTO SeasonResults (SchoolName,Year,GameOfYear,Date,Time,Day,HomeOrAway
        ,Opponent,Outcome,PointsFor,PointsAgainst,Wins,Losses,Streak)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (schoolName,year,gameOfYear,date,time,day,homeOrAway,opponent,outcome\
        ,pointsFor,pointsAgainst,wins,losses,streak)
        )

    
    conn.commit()
    
    conn.close()


###############################################################################

#This section iterates through weblinks using the school list above which contain conference and coach data 
#and populates the Conference and Coach data in the database 
print ('Populating the SeasonResults table. This may take several hours.')

for college in colleges:
    
    collegeName = str(college)
        
    year = thisYear
    
    while year <= currentSchoolYear:
               
        collegeURL = ('http://www.sports-reference.com/cfb/schools/'+college\
        +'/'+str(year)+'-schedule.html')
        
        try: collegeStatsHTML = urllib.request.urlopen(collegeURL).read()
        except: 
            year = year + 1
            continue
        
        collegeStatsSoup = BeautifulSoup(collegeStatsHTML, 'html.parser')
        collegeStatsTags = collegeStatsSoup('table', id='team')  
        collegeStatsTags = collegeStatsSoup('td')  
        
        gameOfYear = 1
        timeOfDay = ''
        dateOfGame = ''
        day = ''
        homeOrAway = ''
        opponent = ''
        outcome = ''
        pointsFor = ''
        pointsAgainst = ''
        wins = ''
        losses = ''
        streak = ''
        
        x = 0
        run = 0
        
        if year >= 2013:
        
            for tag in collegeStatsTags:
                
                if re.search('/cfb/boxscores/',str(tag.contents)): 
                    run = 1
         
                if run == 1:
                    if x == 0:
                        dateOfGame = str(re.findall('[A-Z]+.+<',str(tag.contents)))[2:-3]
                    elif x == 1:
                        timeOfDay = (str(tag.contents)[2:-2])
                    elif x == 2:
                        day = (str(tag.contents)[2:-2])
                    elif x == 4:
                        homeOrAway = (str(tag.contents)[2:-2])
                        if homeOrAway == '@':
                            homeOrAway = 'Away'
                        elif homeOrAway == 'N':
                            homeOrAway = 'Neutral'
                        else: homeOrAway = 'Home'
                    elif x == 5:
                        if re.search('/cfb/schools/',str(tag.contents)):
                            opponentString = re.findall('[A-Z]+.+<',str(tag.contents))
                            opponent = str(opponentString)[2:-3]
                        else:
                            opponent = str(tag.contents)[2:-2]
                        opponent = re.sub('[()]','', opponent)
                        opponent = re.sub('&amp;','', opponent)
                    elif x == 7:
                        outcome = (str(tag.contents)[2:-2])
                    elif x == 8:
                        pointsFor = (str(tag.contents)[2:-2])
                    elif x == 9:
                        pointsAgainst = (str(tag.contents)[2:-2])
                    elif x == 10:
                        wins = (str(tag.contents)[2:-2])
                    elif x == 11:
                        losses = (str(tag.contents)[2:-2])
                    elif x == 12:
                        streak = (str(tag.contents)[2:-2])
                        
                    x = x + 1 
                    
                    if x == 13:     
                        PushToSeasonResults(collegeName,year,gameOfYear,dateOfGame,timeOfDay,day\
                        ,homeOrAway,opponent,outcome,pointsFor,pointsAgainst,wins,losses,streak)
                        
                        x = 0
                        run = 0
                        gameOfYear = gameOfYear + 1
        
            year = year + 1
            
        else:
            
            for tag in collegeStatsTags:
                
                if re.search('/cfb/boxscores/',str(tag.contents)): 
                    run = 1
                   
                if run == 1:
                    if x == 0:
                        dateOfGame = str(re.findall('[A-Z]+.+<',str(tag.contents)))[2:-3]
                    elif x == 1:
                        day = (str(tag.contents)[2:-2])
                    elif x == 3:
                        homeOrAway = (str(tag.contents)[2:-2])
                        if homeOrAway == '@':
                            homeOrAway = 'Away'
                        elif homeOrAway == 'N':
                            homeOrAway = 'Neutral'
                        else: homeOrAway = 'Home'
                    elif x == 4:
                        if re.search('/cfb/schools/',str(tag.contents)):
                            opponentString = re.findall('[A-Z]+.+<',str(tag.contents))
                            opponent = str(opponentString)[2:-3]
                        else:
                            opponent = str(tag.contents)[2:-2]
                        opponent = re.sub('[()]','', opponent)
                        opponent = re.sub('&amp;','', opponent)
                    elif x == 6:
                        outcome = (str(tag.contents)[2:-2])
                    elif x == 7:
                        pointsFor = (str(tag.contents)[2:-2])
                    elif x == 8:
                        pointsAgainst = (str(tag.contents)[2:-2])
                    elif x == 9:
                        wins = (str(tag.contents)[2:-2])
                    elif x == 10:
                        losses = (str(tag.contents)[2:-2])
                    elif x == 11:
                        streak = (str(tag.contents)[2:-2])
                        
                    x = x + 1 
                    
                    if x == 13:     
                        PushToSeasonResults(collegeName,year,gameOfYear,dateOfGame,'Unknown'\
                        ,day,homeOrAway,opponent,outcome,pointsFor,pointsAgainst,wins,losses,streak)
                        
                        x = 0
                        run = 0
                        gameOfYear = gameOfYear + 1

        
            year = year + 1
            
print ("SeasonResults table has been populated")

        
print (time.asctime(time.localtime(time.time())))
