import urllib.request
from urllib.error import URLError, HTTPError
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

DROP TABLE IF EXISTS GameResults;

CREATE TABLE GameResults (
    SchoolName TEXT
    ,Year INTEGER
    ,GameDate TEXT
    ,Opponent TEXT
    ,TotalYards INTEGER 
    ,TotalPlays INTEGER
    ,YdsPerPlay REAL
    ,PassingYds INTEGER
    ,CompletionsAndAttempts TEXT
    ,YdsPerPass REAL
    ,RushingYds INTEGER
    ,Rushes INTEGER
    ,YdsPerRush REAL
    ,FirstDowns INTEGER
    ,FirstDownsByPass INTEGER
    ,FirstDownsByRush INTEGER
    ,FirstDownsByPenalty INTEGER
    ,Penatlies INTEGER
    ,PenaltyYards INTEGER
    ,Turnovers INTEGER
    ,FumblesLost INTEGER
    ,InterceptionsThrown INTEGER
    ,OpponentTotalYards INTEGER
    ,OpponentTotalPlays INTEGER
    ,OpponentYdsPerPlay REAL
    ,OpponentPassingYds INTEGER
    ,OpponentCompletionsAndAttempts TEXT
    ,OpponentYdsPerPass REAL
    ,OpponentRushingYds INTEGER
    ,OpponentRushes INTEGER
    ,OpponentYdsPerRush REAL
    ,OpponentFirstDowns INTEGER
    ,OpponentFirstDownsByPass INTEGER
    ,OpponentFirstDownsByRush INTEGER
    ,OpponentFirstDownsByPenalty INTEGER
    ,OpponentPenatlies INTEGER
    ,OpponentPenaltyYards INTEGER
    ,OpponentTurnovers INTEGER
    ,OpponentFumblesLost INTEGER
    ,OpponentInterceptionsThrown INTEGER
)

''')

print ('Table Created')

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

else: colleges = ['georgia']

print ('Done with Schools')

################################################################################

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
    print (opponentName)
    
    if homeOrAway == 'Home':
        gameURL = 'http://www.sports-reference.com/cfb/boxscores/'+newDate+\
        '-'+collegeName+'.html'
        try:
            gameHTML = urllib.request.urlopen(gameURL).read()
        except HTTPError as e:
                print('HTTPError Code: ', e.code)
        except URLError as e:
                print('URLError Reason: ', e.reason)
    elif homeOrAway == 'Away':
        gameURL = 'http://www.sports-reference.com/cfb/boxscores/'+newDate+\
        '-'+opponentName+'.html'
        try:
            gameHTML = urllib.request.urlopen(gameURL).read()
        except HTTPError as e:
                print('HTTPError Code: ', e.code)
        except URLError as e:
                print('URLError Reason: ', e.reason)
    else:
        gameURL = 'http://www.sports-reference.com/cfb/boxscores/'+newDate+\
        '-'+collegeName+'.html'
        try:
            response = urllib.request.urlopen(gameURL)
            if response.geturl() == gameURL:   
                gameHTML = response.read()
            else:
                gameURL = 'http://www.sports-reference.com/cfb/boxscores/'+newDate+\
                '-'+opponentName+'.html'
                gameHTML = urllib.request.urlopen(gameURL).read()
        except HTTPError as e:
                print('HTTPError Code: ', e.code)
        except URLError as e:
                print('URLError Reason: ', e.reason)            

                               
    print (gameURL)
    
    gameSoup = BeautifulSoup(gameHTML, 'html.parser')
    
    gameTags = gameSoup('td', {'class' : 'align_center'})
    
    totalYards = ''
    totalPlays = ''
    ydsPerPlay = ''
    passingYds = ''
    completionsAndAttempts = ''
    ydsPerPass = ''
    rushingYds = ''
    rushes = ''
    ydsPerRush = ''
    firstDowns = ''
    firstDownsByPass = ''
    firstDownsByRush = ''
    firstDownsByPenalty = ''
    penalties = ''
    penaltyYds = ''
    turnovers = ''
    fumblesLost = ''
    interceptionsThrown = ''
    
    opponent_totalYards = ''
    opponent_totalPlays = ''
    opponent_ydsPerPlay = ''
    opponent_passingYds = ''
    opponent_completionsAndAttempts = ''
    opponent_ydsPerPass = ''
    opponent_rushingYds = ''
    opponent_rushes = ''
    opponent_ydsPerRush = ''
    opponent_firstDowns = ''
    opponent_firstDownsByPass = ''
    opponent_firstDownsByRush = ''
    opponent_firstDownsByPenalty = ''
    opponent_penalties = ''
    opponent_penaltyYds = ''
    opponent_turnovers = ''
    opponent_fumblesLost = ''
    opponent_interceptionsThrown = ''


    conn = sqlite3.connect('BettingData.db')
    cur = conn.cursor()

    z = 1   
    
    for tag in gameTags:
#        print (tag.contents)
        thisTag = re.findall('r>.+</b',str(tag))
        thisTag = str(thisTag)[4:-5]
        
        if z == 2:
            totalYards = thisTag
        elif z == 3:
            opponent_totalYards = thisTag
        elif z == 5:
            totalPlays = thisTag
        elif z == 6:
            opponent_totalPlays = thisTag
        elif z == 8:
            ydsPerPlay = thisTag
        elif z == 9:
            opponent_ydsPerPlay = thisTag
        elif z == 11:
            passingYds = thisTag
        elif z == 12:
            opponent_passingYds = thisTag
        elif z == 14:
            completionsAndAttempts = thisTag
        elif z == 15:
            opponent_completionsAndAttempts = thisTag
        elif z == 17:
            ydsPerPass = thisTag
        elif z == 18:
            opponent_ydsPerPass = thisTag
        elif z == 20:
            rushingYds = thisTag
        elif z == 21:
            opponent_rushingYds
        elif z == 23:
            rushes = thisTag
        elif z == 24:
            opponent_rushes = thisTag
        elif z == 26:
            ydsPerRush = thisTag
        elif z == 27:
            opponent_ydsPerRush = thisTag
        elif z == 29:
            firstDowns = thisTag
        elif z == 30:
            opponent_firstDowns = thisTag
        elif z == 32:
            firstDownsByPass = thisTag
        elif z == 33:
            opponent_firstDownsByPass = thisTag
        elif z == 35:
            firstDownsByRush = thisTag
        elif z == 36:
            opponent_firstDownsByRush = thisTag
        elif z == 38:
            firstDownsByPenalty = thisTag
        elif z == 39:
            opponent_firstDownsByPenalty = thisTag
        elif z == 41:
            penalties = thisTag
        elif z == 42:
            opponent_penalties = thisTag
        elif z == 44:
            penaltyYds = thisTag
        elif z == 45:
            opponent_penaltyYds = thisTag
        elif z == 47:
            turnovers = thisTag
        elif z == 48:
            opponent_turnovers = thisTag
        elif z == 50:
            fumblesLost = thisTag
        elif z == 51:
            opponent_fumblesLost = thisTag
        elif z == 53:
            interceptionsThrown = thisTag
        elif z == 54: 
            opponent_interceptionsThrown = thisTag
            
        z = z + 1
            
    cur.execute('''
        INSERT INTO GameResults (SchoolName,Year,GameDate,Opponent,TotalYards 
        ,TotalPlays,YdsPerPlay,PassingYds,CompletionsAndAttempts,YdsPerPass
        ,RushingYds,Rushes,YdsPerRush,FirstDowns,FirstDownsByPass,FirstDownsByRush
        ,FirstDownsByPenalty,Penatlies,PenaltyYards,Turnovers,FumblesLost
        ,InterceptionsThrown,OpponentTotalYards,OpponentTotalPlays,OpponentYdsPerPlay
        ,OpponentPassingYds,OpponentCompletionsAndAttempts,OpponentYdsPerPass
        ,OpponentRushingYds,OpponentRushes,OpponentYdsPerRush,OpponentFirstDowns
        ,OpponentFirstDownsByPass,OpponentFirstDownsByRush,OpponentFirstDownsByPenalty
        ,OpponentPenatlies,OpponentPenaltyYards,OpponentTurnovers,OpponentFumblesLost
        ,OpponentInterceptionsThrown)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (collegeName,year,aDate,opponent,totalYards,totalPlays,ydsPerPlay,passingYds,completionsAndAttempts\
        ,ydsPerPass,rushingYds,rushes,ydsPerRush,firstDowns,firstDownsByPass,firstDownsByRush\
        ,firstDownsByPenalty,penalties,penaltyYds,turnovers,fumblesLost,interceptionsThrown\
        ,opponent_totalYards,opponent_totalPlays,opponent_ydsPerPlay,opponent_passingYds\
        ,opponent_completionsAndAttempts,opponent_ydsPerPass,opponent_rushingYds,opponent_rushes\
        ,opponent_ydsPerRush,opponent_firstDowns,opponent_firstDownsByPass,opponent_firstDownsByRush\
        ,opponent_firstDownsByPenalty,opponent_penalties,opponent_penaltyYds,opponent_turnovers\
        ,opponent_fumblesLost,opponent_interceptionsThrown)
        )
        
    print ('Written')
    
    conn.commit()
    
    conn.close()
    
 ###############################################################################

for college in colleges:
    
    print (college)
    collegeName = str(college)
        
    year = thisYear
    
    while year <= 2015:
        
        print (year)

        collegeURL = ('http://www.sports-reference.com/cfb/schools/'+college\
        +'/'+str(year)+'-schedule.html')
        
#        print (collegeURL)
        
        try: collegeStatsHTML = urllib.request.urlopen(collegeURL).read()
        except: continue
        
        collegeStatsSoup = BeautifulSoup(collegeStatsHTML, 'html.parser')
    #    collegeStatsTags = collegeStatsSoup('table', id='team')  
        collegeStatsTags = collegeStatsSoup('td')  
        
        gameOfYear = 1
        timeOfDay = ''
        dateOfGame = ''
        day = ''
        homeOrAway = ''
        opponent = ''
        
        x = 0
        run = 0
#        y = 0
        
        if year >= 2013:
        
            for tag in collegeStatsTags:
    #            print ('Tag:',tag)
            
    #            print (gameOfYear)
                
                if re.search('/cfb/boxscores/',str(tag.contents)): 
                    run = 1
    
    #            print ('TagContents:',tag.contents)
    #               
                if run == 1:
                    if x == 0:
                        dateOfGame = str(re.findall('[A-Z]+.+<',str(tag.contents)))[2:-3]
    #                    print ('Date:',dateOfGame)
                    elif x == 1:
                        timeOfDay = (str(tag.contents)[2:-2])
    #                    print ('Time:',time)
                    elif x == 2:
                        day = (str(tag.contents)[2:-2])
    #                    print ('Day:',day)
                    elif x == 4:
                        homeOrAway = (str(tag.contents)[2:-2])
                        if homeOrAway == '@':
                            homeOrAway = 'Away'
                        elif homeOrAway == 'N':
                            homeOrAway = 'Neutral'
                        else: homeOrAway = 'Home'
    #                    print ('HomeOrAway:',homeOrAway)
                    elif x == 5:
    #                    print (tag.contents)
                        if re.search('/cfb/schools/',str(tag.contents)):
                            opponentString = re.findall('[A-Z]+.+<',str(tag.contents))
                            opponent = str(opponentString)[2:-3]
                        else:
                            opponent = str(tag.contents)[2:-2]
                        opponent = re.sub('[()]','', opponent)
                        opponent = re.sub('&amp;','', opponent)
                        time.sleep(30)
                        RetrieveGameStats(collegeName,year,dateOfGame,opponent,homeOrAway)
    #                    print ('Opponent:',opponent)
                        
                    x = x + 1 
    #                print ('X:',x)
                    
                    if x == 6:     
                        
                        x = 0
                        run = 0
                        gameOfYear = gameOfYear + 1
        
            year = year + 1
            time.sleep(300)
            
        else:
            
            for tag in collegeStatsTags:
    #            print ('Tag:',tag)
            
    #            print (gameOfYear)
                
                if re.search('/cfb/boxscores/',str(tag.contents)): 
                    run = 1
    
    #            print ('TagContents:',tag.contents)
    #               
                if run == 1:
                    if x == 0:
                        dateOfGame = str(re.findall('[A-Z]+.+<',str(tag.contents)))[2:-3]
    #                    print ('Date:',dateOfGame)
                    elif x == 1:
                        day = (str(tag.contents)[2:-2])
    #                    print ('Day:',day)
                    elif x == 3:
                        homeOrAway = (str(tag.contents)[2:-2])
                        if homeOrAway == '@':
                            homeOrAway = 'Away'
                        elif homeOrAway == 'N':
                            homeOrAway = 'Neutral'
                        else: homeOrAway = 'Home'
    #                    print ('HomeOrAway:',homeOrAway)
                    elif x == 4:
    #                    print (tag.contents)
                        if re.search('/cfb/schools/',str(tag.contents)):
                            opponentString = re.findall('[A-Z]+.+<',str(tag.contents))
                            opponent = str(opponentString)[2:-3]
                        else:
                            opponent = str(tag.contents)[2:-2]
                        opponent = re.sub('[()]','', opponent)
                        opponent = re.sub('&amp;','', opponent)
                        time.sleep(30)
                        RetrieveGameStats(collegeName,year,dateOfGame,opponent,homeOrAway)
    #                    print ('Opponent:',opponent)
                        
                    x = x + 1 
    #                print ('X:',x)30th
                    
                    if x == 5:                            
                        x = 0
                        run = 0
                        gameOfYear = gameOfYear + 1

        
            year = year + 1
            time.sleep(120)
            

        
print (time.asctime(time.localtime(time.time())))
