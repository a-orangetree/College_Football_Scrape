import urllib.request
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup
import sqlite3
import re
import time


# currentSchoolYear should be year which the current or last college football season began.
# So, if it is the 2016-2017 season, you would enter 2016.
currentSchoolYear = 2016

# Used for testing. If "Yes" only a subsection of schools will be scraped and populated in the database
isThisATest = 'no'


##################################################################################
# Below creates tables ready to receive data for the GameResults table
print (time.asctime(time.localtime(time.time())))
thisYear = (currentSchoolYear - 9)

conn = sqlite3.connect('CFBData.db')
cur = conn.cursor()

cur.executescript('''

DROP TABLE IF EXISTS GameResults;

CREATE TABLE GameResults (
    SchoolName TEXT
    ,Year INTEGER
    ,GameDate TEXT
    ,Opponent TEXT
    ,HomeOrAway TEXT
    ,TotalYards INTEGER
    ,TotalRushes INTEGER
    ,RushingYards INTEGER
    ,RushingTDs INTEGER
    ,NumberOfPassingAtmpts INTEGER
    ,PassingCompletions INTEGER
    ,PassingYards INTEGER
    ,PassingTDs INTEGER
    ,PassingINTs INTEGER
    ,FirstDowns INTEGER
    ,NumberOfFumbles INTEGER
    ,LostFumbles INTEGER
    ,Turnovers INTEGER
    ,NumberOfPenalties INTEGER
    ,PenaltyYards INTEGER
    ,opponentTotalYards INTEGER
    ,opponentTotalRushes INTEGER
    ,opponentRushingYards INTEGER
    ,opponentRushingTDs INTEGER
    ,opponentNumberOfPassingAtmpts INTEGER
    ,opponentPassingCompletions INTEGER
    ,opponentPassingYards INTEGER
    ,opponentPassingTDs INTEGER
    ,opponentPassingINTs INTEGER
    ,opponentFirstDowns INTEGER
    ,opponentNumberOfFumbles INTEGER
    ,opponentLostFumbles INTEGER
    ,opponentTurnovers INTEGER
    ,opponentNumberOfPenalties INTEGER
    ,opponentPenaltyYards INTEGER
)

''')

print ('An empty GameResults table has been created')

conn.close()



###############################################################################


#This section creates a list of schools playing in the current school year
#The list is used to generate weblinks which are visited and scraped below
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
        if re.search('2016', str(tag)):
            colleges.append(collegesString)
        else: continue

else: colleges = ['kent-state']

print ('Created a list of schools')

################################################################################


#Defines a function to populate data in the GameResults table. The function is called in the next section.
def RetrieveGameStats(collegeName,year,aDate,opponent,homeOrAway):
    
    newYear = aDate[7:]
    
    newMonth = aDate[:3]
    
    if newMonth == 'Jan':
        newMonth = '01'
    if newMonth == 'Feb':
        newMonth = '02'
    if newMonth == 'Mar':
        newMonth = '03'
    if newMonth == 'Apr':
        newMonth = '04'
    if newMonth == 'May':
        newMonth = '05'
    if newMonth == 'Jun':
        newMonth = '06'
    if newMonth == 'Jul':
        newMonth = '07'
    if newMonth == 'Aug':
        newMonth = '08'
    if newMonth == 'Sep':
        newMonth = '09'
    if newMonth == 'Oct':
        newMonth = '10'
    if newMonth == 'Nov':
        newMonth = '11'
    if newMonth == 'Dec':
        newMonth = '12'
        
    if len(aDate) == 11:
        newDay = '0'+aDate[4:5]
        
    elif len(aDate) == 12:
        newDay = aDate[4:6]
        
    newDate = (newYear.strip()+'-'+newMonth.strip()+'-'+newDay.strip())
    
    opponentName = str(opponent).lower()
    opponentName = re.sub('\s','-',opponentName)
    opponentName = re.sub('_','-',opponentName)
    opponentName = re.sub('[()]','',opponentName)
    
    
    if homeOrAway == 'Home':
        gameURL = 'http://www.sports-reference.com/cfb/boxscores/'+newDate+\
        '-'+collegeName+'.html'
        try:
            #print('1')
            gameHTML = urllib.request.urlopen(gameURL).read()
        except HTTPError as e:
            #print('HTTPError Code: ', e.code)
            return
        except URLError as e:
            #print('URLError Reason: ', e.reason)
            return
            
    elif homeOrAway == 'Away':
        gameURL = 'http://www.sports-reference.com/cfb/boxscores/'+newDate+\
        '-'+opponentName+'.html'
        try:
            #print('2')
            gameHTML = urllib.request.urlopen(gameURL).read()
        except HTTPError as e:
            #print('HTTPError Code: ', e.code)
            return
        except URLError as e:
            #print('URLError Reason: ', e.reason)
            return
    else:
        gameURL = 'http://www.sports-reference.com/cfb/boxscores/'+newDate+\
        '-'+collegeName+'.html'
        try:
            #print('3')
            gameHTML = urllib.request.urlopen(gameURL).read()
        except HTTPError as e:
            #print('HTTPError Code: ', e.code)
            gameURL = 'http://www.sports-reference.com/cfb/boxscores/'+newDate+\
            '-'+opponentName+'.html'
            gameHTML = urllib.request.urlopen(gameURL).read()
        except URLError as e:
            #print('URLError Reason: ', e.reason)
            gameURL = 'http://www.sports-reference.com/cfb/boxscores/'+newDate+\
            '-'+opponentName+'.html'
            gameHTML = urllib.request.urlopen(gameURL).read()
     
                  
    FirstDownsHome = ''
    NumberOfRushesHome = ''
    RushingYardsHome = ''
    RushingTDsHome = ''
    PassingCompletionsHome = ''
    PassingAttemptsHome = ''
    PassingYardsHome = ''
    PassingTDsHome = ''
    PassingINTsHome = ''
    TotalYardsHome = ''
    NumberOfFumblesHome = ''
    LostFumblesHome = ''
    TurnoversHome = ''
    NumberOfPenaltiesHome = ''
    YardsOfPenaltiesHome = ''
    
    FirstDownsVisitor = ''
    NumberOfRushesVisitor = ''
    RushingYardsVisitor = ''
    RushingTDsVisitor = ''
    PassingCompletionsVisitor = ''
    PassingAttemptsVisitor = ''
    PassingYardsVisitor = ''
    PassingTDsVisitor = ''
    PassingINTsVisitor = ''
    TotalYardsVisitor = ''
    NumberOfFumblesVisitor = ''
    LostFumblesVisitor = ''
    TurnoversVisitor = '' 
    NumberOfPenaltiesVisitor = ''
    YardsOfPenaltiesVisitor = ''
    
    
    gameSoup = BeautifulSoup(gameHTML, 'html.parser')
    
    gameTags = gameSoup('div', {'id' : 'all_team_stats'})
    
    for tag in gameTags:
        FirstDowns = re.findall('First Downs.+?</tr',str(tag.contents))
        FirstDowns = re.findall('>\d+.*?<',str(FirstDowns))
        FirstDownsHome = str(FirstDowns[0])[1:-1]
        FirstDownsVisitor = str(FirstDowns[1])[1:-1]                     
        
        Rushing = re.findall('Rush-Yds-TDs.+?</tr',str(tag.contents))
        Rushing = re.findall('>\d+.*?<',str(Rushing))
        
        RushingHome = str(Rushing[0])[1:-1]
        RushingHome = re.split('-?', RushingHome)
        if ('' in RushingHome): RushingHome.remove('')
        NumberOfRushesHome = RushingHome[0]
        RushingYardsHome = RushingHome[1]
        RushingTDsHome = RushingHome[2]

        RushingVisitor = str(Rushing[1])[1:-1]
        RushingVisitor = re.split('-?', RushingVisitor)
        if ('' in RushingVisitor): RushingVisitor.remove('')
        NumberOfRushesVisitor = RushingVisitor[0]
        RushingYardsVisitor = RushingVisitor[1]
        RushingTDsVisitor = RushingVisitor[2]
        
        Passing = re.findall('Cmp-Att-Yd-TD-INT.+?</tr',str(tag.contents))
        Passing = re.findall('>\d+.*?<',str(Passing))
        
        PassingHome = str(Passing[0])[1:-1]
        PassingHome = re.split('-?', PassingHome)
        if ('' in PassingHome): PassingHome.remove('')
        PassingCompletionsHome = PassingHome[0]
        PassingAttemptsHome = PassingHome[1]
        PassingYardsHome = PassingHome[2]
        PassingTDsHome = PassingHome[3]
        PassingINTsHome = PassingHome[4]

        PassingVisitor = str(Passing[1])[1:-1]
        PassingVisitor = re.split('-?', PassingVisitor)
        if ('' in PassingVisitor): PassingVisitor.remove('')
        PassingCompletionsVisitor = PassingVisitor[0]
        PassingAttemptsVisitor = PassingHome[1]
        PassingYardsVisitor = PassingVisitor[2]
        PassingTDsVisitor = PassingVisitor[3]
        PassingINTsVisitor = PassingVisitor[4]
        
        TotalYards = re.findall('Total Yards.+?</tr',str(tag.contents))
        TotalYards = re.findall('>-*\d+.*?<',str(TotalYards))
        
        TotalYardsHome = str(TotalYards[0])[1:-1]
                             
        TotalYardsVisitor = str(TotalYards[1])[1:-1]
        
        FumblesLost = re.findall('Fumbles-Lost.+?</tr',str(tag.contents))
        FumblesLost = re.findall('>\d+.*?<',str(FumblesLost))
        
        FumblesLostHome = str(FumblesLost[0])[1:-1]
        FumblesLostHome = FumblesLostHome.split('-')
        NumberOfFumblesHome = FumblesLostHome[0]
        LostFumblesHome = FumblesLostHome[1]

        FumblesLostVisitor = str(FumblesLost[1])[1:-1]
        FumblesLostVisitor = FumblesLostVisitor.split('-')
        NumberOfFumblesVisitor = FumblesLostVisitor[0]
        LostFumblesVisitor = FumblesLostVisitor[1]
        
        Turnovers = re.findall('Turnovers.+?</tr',str(tag.contents))
        Turnovers = re.findall('>\d+.*?<',str(Turnovers))
        
        TurnoversHome = str(Turnovers[0])[1:-1]
                            
        TurnoversVisitor = str(Turnovers[1])[1:-1]
        
        PenaltiesYards = re.findall('Penalties-Yards.+?</tr',str(tag.contents))
        PenaltiesYards = re.findall('>\d+.*?<',str(PenaltiesYards))
        
        PenaltiesYardsHome = str(PenaltiesYards[0])[1:-1]
        PenaltiesYardsHome = PenaltiesYardsHome.split('-')
        NumberOfPenaltiesHome = PenaltiesYardsHome[0]
        YardsOfPenaltiesHome = PenaltiesYardsHome[1]

        PenaltiesYardsVisitor = str(PenaltiesYards[1])[1:-1]
        PenaltiesYardsVisitor = PenaltiesYardsVisitor.split('-')
        NumberOfPenaltiesVisitor = PenaltiesYardsVisitor[0]
        YardsOfPenaltiesVisitor = PenaltiesYardsVisitor[1]

    
    conn = sqlite3.connect('CFBData.db')
    cur = conn.cursor()  
       
    ## The Away and Home indicators attached to each variable were mistakenly swapped
    if homeOrAway == 'Away':
            
        cur.execute('''
            INSERT INTO GameResults (SchoolName,Year,GameDate,Opponent,HomeOrAway,
            TotalYards, TotalRushes, RushingYards, RushingTDs,NumberOfPassingAtmpts,
            PassingCompletions, PassingYards, PassingTDs, PassingINTs, FirstDowns, NumberOfFumbles,
            LostFumbles, Turnovers, NumberOfPenalties, PenaltyYards, opponentTotalYards, 
            opponentTotalRushes, opponentRushingYards, opponentRushingTDs, 
            opponentNumberOfPassingAtmpts, opponentPassingCompletions,
            opponentPassingYards, opponentPassingTDs, opponentPassingINTs, opponentFirstDowns,
            opponentNumberOfFumbles, opponentLostFumbles, opponentTurnovers, 
            opponentNumberOfPenalties, opponentPenaltyYards)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (collegeName, year, aDate, opponent, homeOrAway,\
              TotalYardsHome, NumberOfRushesHome, RushingYardsHome, RushingTDsHome,\
              PassingAttemptsHome, PassingCompletionsHome, PassingYardsHome, PassingTDsHome,\
              PassingINTsHome, FirstDownsHome, NumberOfFumblesHome, LostFumblesHome,\
              TurnoversHome, NumberOfPenaltiesHome, YardsOfPenaltiesHome,\
              TotalYardsVisitor, NumberOfRushesVisitor, RushingYardsVisitor, RushingTDsVisitor,\
              PassingAttemptsVisitor, PassingCompletionsVisitor, PassingYardsVisitor,\
              PassingTDsVisitor, PassingINTsVisitor, FirstDownsVisitor, NumberOfFumblesVisitor,\
              LostFumblesVisitor, TurnoversVisitor, NumberOfPenaltiesVisitor, YardsOfPenaltiesVisitor)
            )
    elif homeOrAway == 'Home':
        
        cur.execute('''
            INSERT INTO GameResults (SchoolName,Year,GameDate,Opponent,HomeOrAway,
            TotalYards, TotalRushes, RushingYards, RushingTDs,NumberOfPassingAtmpts,
            PassingCompletions, PassingYards, PassingTDs, PassingINTs, FirstDowns, NumberOfFumbles,
            LostFumbles, Turnovers, NumberOfPenalties, PenaltyYards, opponentTotalYards, 
            opponentTotalRushes, opponentRushingYards, opponentRushingTDs, 
            opponentNumberOfPassingAtmpts, opponentPassingCompletions,
            opponentPassingYards, opponentPassingTDs, opponentPassingINTs, opponentFirstDowns,
            opponentNumberOfFumbles, opponentLostFumbles, opponentTurnovers, 
            opponentNumberOfPenalties, opponentPenaltyYards)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (collegeName, year, aDate, opponent, homeOrAway,\
              TotalYardsVisitor, NumberOfRushesVisitor, RushingYardsVisitor, RushingTDsVisitor,\
              PassingAttemptsVisitor, PassingCompletionsVisitor, PassingYardsVisitor,\
              PassingTDsVisitor, PassingINTsVisitor, FirstDownsVisitor, NumberOfFumblesVisitor,\
              LostFumblesVisitor, TurnoversVisitor, NumberOfPenaltiesVisitor, YardsOfPenaltiesVisitor,\
              TotalYardsHome, NumberOfRushesHome, RushingYardsHome, RushingTDsHome,\
              PassingAttemptsHome, PassingCompletionsHome,PassingYardsHome, PassingTDsHome,\
              PassingINTsHome, FirstDownsHome, NumberOfFumblesHome, LostFumblesHome,\
              TurnoversHome, NumberOfPenaltiesHome, YardsOfPenaltiesHome)
            )
            
    else:
        cur.execute('''
            INSERT INTO GameResults (SchoolName,Year,GameDate,Opponent,HomeOrAway,
            TotalYards, TotalRushes, RushingYards, RushingTDs,NumberOfPassingAtmpts,
            PassingCompletions, PassingYards, PassingTDs, PassingINTs, FirstDowns, NumberOfFumbles,
            LostFumbles, Turnovers, NumberOfPenalties, PenaltyYards, opponentTotalYards, 
            opponentTotalRushes, opponentRushingYards, opponentRushingTDs, 
            opponentNumberOfPassingAtmpts, opponentPassingCompletions,
            opponentPassingYards, opponentPassingTDs, opponentPassingINTs, opponentFirstDowns,
            opponentNumberOfFumbles, opponentLostFumbles, opponentTurnovers, 
            opponentNumberOfPenalties, opponentPenaltyYards)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (collegeName, year, aDate, opponent, homeOrAway, '', '', '', '', '', '', '', '', '',\
             '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '')
            )
        
    
    conn.commit()
    
    conn.close()

    
 ###############################################################################

 
#This section iterates through weblinks using the school list above which contain game data 
#and populates the GameResults data in the database 
print ('Populating GameResults table. May take several hours.')

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
        collegeStatsTags = collegeStatsSoup('td')  
        
        gameOfYear = 1
        timeOfDay = ''
        dateOfGame = ''
        day = ''
        homeOrAway = ''
        opponent = ''
        
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
                        RetrieveGameStats(collegeName,year,dateOfGame,opponent,homeOrAway)
                        
                    x = x + 1 
                    if x == 6:     
                        
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
                        RetrieveGameStats(collegeName,year,dateOfGame,opponent,homeOrAway)
                        
                    x = x + 1 
                    
                    if x == 5:                            
                        x = 0
                        run = 0
                        gameOfYear = gameOfYear + 1

        
            year = year + 1
            
            
print ("GameResults table has been populated")          
        
print (time.asctime(time.localtime(time.time())))
