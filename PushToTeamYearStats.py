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
        
        conn.close()
        
        
#########################################################################        

#This section iterates through weblinks using the school list above which contain game data
#and populates the TeamSplits data in the database     
print ('Populating the TeamStatistics table. This may take several hours.')
for college in finalCollegeList:
    
    year = thisYear
    
    while year <= currentSchoolYear:
        
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
        
        opp_PassingCompletions = ''
        opp_PassingAtmpts = ''
        opp_PassingCompletePct = ''
        opp_PassingTotYds = ''
        opp_PassingTDs = ''
        opp_RushingAtmpts = ''
        opp_RushingTotYds = ''
        opp_RushingAvgYds = ''
        opp_RushingTDs = ''
        opp_totalOffensePlays = ''
        opp_totalOffenseTotYds = ''
        opp_totalOffenseAvgYds = ''
        opp_firstDownsByPassing = ''
        opp_firstDownsByRushing = ''
        opp_firstDownsByPenalty = ''
        opp_firstDownsTot = ''
        opp_penaltiesTot = ''
        opp_penaltiesYds = ''
        opp_turnoversByFumble = ''
        opp_turnoversByInt = ''
        opp_turnoversTot = ''
        
        for tag in collegeStatsTags:
            if re.search('data-stat="g"><',str(tag)):
                break
            
            if re.search('data-stat="g"',str(tag)):
                 gamesPlayed = (str(tag.contents)[2:-2])
            elif re.search('data-stat="pass_cmp"',str(tag)):
                PassingCompletions = (str(tag.contents)[2:-2])
            elif re.search('data-stat="pass_att"',str(tag)):
                PassingAtmpts = (str(tag.contents)[2:-2])
            elif re.search('data-stat="pass_cmp_pct"',str(tag)):
                PassingCompletePct = (str(tag.contents)[2:-2])
            elif re.search('data-stat="pass_yds"',str(tag)):
                PassingTotYds = (str(tag.contents)[2:-2])
            elif re.search('data-stat="pass_td"',str(tag)):
                PassingTDs = (str(tag.contents)[2:-2])
            elif re.search('data-stat="rush_att"',str(tag)):
                RushingAtmpts = (str(tag.contents)[2:-2])
            elif re.search('data-stat="rush_yds"',str(tag)):
                RushingTotYds = (str(tag.contents)[2:-2])
            elif re.search('data-stat="rush_yds_per_att"',str(tag)):
                RushingAvgYds = (str(tag.contents)[2:-2])
            elif re.search('data-stat="rush_td"',str(tag)):
                RushingTDs = (str(tag.contents)[2:-2])
            elif re.search('data-stat="tot_plays"',str(tag)):
                totalOffensePlays = (str(tag.contents)[2:-2])
            elif re.search('data-stat="tot_yds"',str(tag)):
                totalOffenseTotYds = (str(tag.contents)[2:-2])
            elif re.search('data-stat="tot_yds_per_play"',str(tag)):
                totalOffenseAvgYds = (str(tag.contents)[2:-2])
            elif re.search('data-stat="first_down_pass"',str(tag)):
                firstDownsByPassing = (str(tag.contents)[2:-2])
            elif re.search('data-stat="first_down_rush"',str(tag)):
                firstDownsByRushing = (str(tag.contents)[2:-2])
            elif re.search('data-stat="first_down_penalty"',str(tag)):
                firstDownsByPenalty = (str(tag.contents)[2:-2])
            elif re.search('data-stat="first_down"',str(tag)):
                firstDownsTot = (str(tag.contents)[2:-2])
            elif re.search('data-stat="penalty"',str(tag)):
                penaltiesTot = (str(tag.contents)[2:-2])
            elif re.search('data-stat="penalty_yds"',str(tag)):
                penaltiesYds = (str(tag.contents)[2:-2])
            elif re.search('data-stat="fumbles_lost"',str(tag)):
                turnoversByFumble = (str(tag.contents)[2:-2])
            elif re.search('data-stat="pass_int"',str(tag)):
                turnoversByInt = (str(tag.contents)[2:-2])
            elif re.search('data-stat="turnovers"',str(tag)):
                turnoversTot = (str(tag.contents)[2:-2])
                
            elif re.search('data-stat="opp_pass_cmp"',str(tag)):
                opp_PassingCompletions = (str(tag.contents)[2:-2])
            elif re.search('data-stat="opp_pass_att"',str(tag)):
                opp_PassingAtmpts = (str(tag.contents)[2:-2])
            elif re.search('data-stat="opp_pass_cmp_pct"',str(tag)):
                opp_PassingCompletePct = (str(tag.contents)[2:-2])
            elif re.search('data-stat="opp_pass_yds"',str(tag)):
                opp_PassingTotYds = (str(tag.contents)[2:-2])
            elif re.search('data-stat="opp_pass_td"',str(tag)):
                opp_PassingTDs = (str(tag.contents)[2:-2])
            elif re.search('data-stat="opp_rush_att"',str(tag)):
                opp_RushingAtmpts = (str(tag.contents)[2:-2])
            elif re.search('data-stat="opp_rush_yds"',str(tag)):
                opp_RushingTotYds = (str(tag.contents)[2:-2])
            elif re.search('data-stat="opp_rush_yds_per_att"',str(tag)):
                opp_RushingAvgYds = (str(tag.contents)[2:-2])
            elif re.search('data-stat="opp_rush_td"',str(tag)):
                opp_RushingTDs = (str(tag.contents)[2:-2])
            elif re.search('data-stat="opp_tot_plays"',str(tag)):
                opp_totalOffensePlays = (str(tag.contents)[2:-2])
            elif re.search('data-stat="opp_tot_yds"',str(tag)):
                opp_totalOffenseTotYds = (str(tag.contents)[2:-2])
            elif re.search('data-stat="opp_tot_yds_per_play"',str(tag)):
                opp_totalOffenseAvgYds = (str(tag.contents)[2:-2])
            elif re.search('data-stat="opp_first_down_pass"',str(tag)):
                opp_firstDownsByPassing = (str(tag.contents)[2:-2])
            elif re.search('data-stat="opp_first_down_rush"',str(tag)):
                opp_firstDownsByRushing = (str(tag.contents)[2:-2])
            elif re.search('data-stat="opp_first_down_penalty"',str(tag)):
                opp_firstDownsByPenalty = (str(tag.contents)[2:-2])
            elif re.search('data-stat="opp_first_down"',str(tag)):
                opp_firstDownsTot = (str(tag.contents)[2:-2])
            elif re.search('data-stat="opp_penalty"',str(tag)):
                opp_penaltiesTot = (str(tag.contents)[2:-2])
            elif re.search('data-stat="opp_penalty_yds"',str(tag)):
                opp_penaltiesYds = (str(tag.contents)[2:-2])
            elif re.search('data-stat="opp_fumbles_lost"',str(tag)):
                opp_turnoversByFumble = (str(tag.contents)[2:-2])
            elif re.search('data-stat="opp_pass_int"',str(tag)):
                opp_turnoversByInt = (str(tag.contents)[2:-2])
            elif re.search('data-stat="opp_turnovers"',str(tag)):
                opp_turnoversTot = (str(tag.contents)[2:-2])
                
        side = 'Defense'           
        
        PushToDB(collegeName,year,side,gamesPlayed,opp_PassingCompletions\
            ,opp_PassingAtmpts,opp_PassingCompletePct,opp_PassingTotYds\
            ,opp_PassingTDs,opp_RushingAtmpts,opp_RushingTotYds,opp_RushingAvgYds\
            ,opp_RushingTDs,opp_totalOffensePlays,opp_totalOffenseTotYds,opp_totalOffenseAvgYds\
            ,opp_firstDownsByPassing,opp_firstDownsByRushing,opp_firstDownsByPenalty,opp_firstDownsTot\
            ,opp_penaltiesTot,opp_penaltiesYds,opp_turnoversByFumble,opp_turnoversByInt,opp_turnoversTot)

        side = 'Offense'           
        
        PushToDB(collegeName,year,side,gamesPlayed,PassingCompletions\
            ,PassingAtmpts,PassingCompletePct,PassingTotYds\
            ,PassingTDs,RushingAtmpts,RushingTotYds,RushingAvgYds\
            ,RushingTDs,totalOffensePlays,totalOffenseTotYds,totalOffenseAvgYds\
            ,firstDownsByPassing,firstDownsByRushing,firstDownsByPenalty,firstDownsTot\
            ,penaltiesTot,penaltiesYds,turnoversByFumble,turnoversByInt,turnoversTot)
         
        year = year + 1

print ("TeamStatistics table has been populated")

print (time.asctime(time.localtime(time.time())))