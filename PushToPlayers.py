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

# Below creates tables ready to receive data for the Player tables
print (time.asctime(time.localtime(time.time())))
thisYear = (currentSchoolYear - 9)

conn = sqlite3.connect('CFBData.db')
cur = conn.cursor()

cur.executescript('''

DROP TABLE IF EXISTS PlayerPassing;
DROP TABLE IF EXISTS PlayerRushingReceiving;
DROP TABLE IF EXISTS PlayerDefense;
DROP TABLE IF EXISTS PlayerKickPuntReturns;
DROP TABLE IF EXISTS PlayerKickingPunting;

CREATE TABLE PlayerPassing (
    SchoolName TEXT
    ,Year TEXT
    ,PlayerName TEXT
    ,PassingCompletions INTEGER
    ,PassingAtmpts INTEGER
    ,PassingCompletePct REAL
    ,PassingTotYds INTEGER
    ,PassingYardsPerAttmpt INTEGER
    ,PassingTDs INTEGER
    ,PassingINTs INTEGER
    ,PasserRating REAL
);   

CREATE TABLE PlayerRushingReceiving (
    SchoolName TEXT
    ,Year TEXT
    ,PlayerName TEXT
    ,RushingAtmpts INTEGER
    ,RushingTotYds INTEGER
    ,RushingAvgYds REAL
    ,RushingTDs INTEGER
    ,Receptions INTEGER
    ,ReceivingTotYds INTEGER
    ,ReceivingAvgYds REAL
    ,ReceivingTDs INTEGER
);   
    
CREATE TABLE PlayerDefense (
    SchoolName TEXT
    ,Year TEXT
    ,PlayerName TEXT
    ,SoloTackles REAL
    ,AssistedTackles REAL
    ,TotalTackles REAL
    ,TacklesForLoss REAL
    ,Sacks REAL
    ,Interceptions INTEGER
    ,PassesDefended INTEGER
    ,FumblesRecovered INTEGER
    ,ForcedFumbles INTEGER
);

CREATE TABLE PlayerKickPuntReturns (
    SchoolName TEXT
    ,Year TEXT
    ,PlayerName TEXT
    ,KickoffReturns INTEGER
    ,KickoffReturnYds INTEGER
    ,KickoffReturnAvgYds REAL
    ,KickoffReturnTDs INTEGER
    ,PuntReturns INTEGER
    ,PuntReturnYds INTEGER
    ,PuntReturnAvgYds REAL
    ,PuntReturnTDs INTEGER
);

CREATE TABLE PlayerKickingPunting (
    SchoolName TEXT
    ,Year TEXT
    ,PlayerName TEXT
    ,ExtraPointsMade INTEGER
    ,ExtraPointsAttempted INTEGER
    ,ExtraPointsPct REAL
    ,FieldGoalsMade INTEGER
    ,FieldGoalsAttempted INTEGER
    ,FieldGoalsPct REAL
    ,Punts INTEGER
    ,PuntsYds INTEGER
    ,PuntsAvgYds REAL
);
                            
''')

print ('Empty Player tables has been created')


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
        
   
else: finalCollegeList = ['florida-international']


print ('Created a list of schools')    

################################################################################



#Defines a function to populate data in the PlayerPassing table. The function is called in the next section. 
def PushToPassing(SchoolName,Year,PlayerName,PassingCompletions\
            ,PassingAtmpts,PassingCompletePct,PassingTotYds,PassingYardsPerAttmpt\
            ,PassingTDs,PassingINTs,PasserRating):
        
        conn = sqlite3.connect('CFBData.db')
        cur = conn.cursor()
    
        cur.execute('''
            INSERT INTO PlayerPassing(SchoolName,Year,PlayerName,PassingCompletions
            ,PassingAtmpts,PassingCompletePct,PassingTotYds,PassingYardsPerAttmpt
            ,PassingTDs,PassingINTs,PasserRating)
            VALUES (?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (SchoolName,Year,PlayerName,PassingCompletions\
            ,PassingAtmpts,PassingCompletePct,PassingTotYds,PassingYardsPerAttmpt\
            ,PassingTDs,PassingINTs,PasserRating)
            )
        
        conn.commit()
        
        conn.close()
        
        
######################################################################### 

#Defines a function to populate data in the PlayerRushingReceiving table. The function is called in the next section. 
def PushToRushingReceiving(SchoolName,Year,PlayerName,RushingAtmpts\
            ,RushingTotYds,RushingAvgYds,RushingTDs,Receptions,ReceivingTotYds\
            ,ReceivingAvgYds,ReceivingTDs):
        
        conn = sqlite3.connect('CFBData.db')
        cur = conn.cursor()
    
        cur.execute('''
            INSERT INTO PlayerRushingReceiving(SchoolName,Year,PlayerName,RushingAtmpts
            ,RushingTotYds,RushingAvgYds,RushingTDs,Receptions,ReceivingTotYds
            ,ReceivingAvgYds,ReceivingTDs)
            VALUES (?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (SchoolName,Year,PlayerName,RushingAtmpts\
            ,RushingTotYds,RushingAvgYds,RushingTDs,Receptions,ReceivingTotYds\
            ,ReceivingAvgYds,ReceivingTDs)
            )
        
        conn.commit()
        
        conn.close()
        
        
#########################################################################   

#Defines a function to populate data in the PlayerDefense table. The function is called in the next section. 
def PushToDefense(SchoolName,Year,PlayerName,SoloTackles,AssistedTackles\
            ,TotalTackles,TacklesForLoss,Sacks,Interceptions,PassesDefended,FumblesRecovered\
            ,ForcedFumbles):
        
        conn = sqlite3.connect('CFBData.db')
        cur = conn.cursor()
    
        cur.execute('''
            INSERT INTO PlayerDefense(SchoolName,Year,PlayerName,SoloTackles,AssistedTackles
            ,TotalTackles,TacklesForLoss,Sacks,Interceptions,PassesDefended,FumblesRecovered
            ,ForcedFumbles)
            VALUES (?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (SchoolName,Year,PlayerName,SoloTackles,AssistedTackles\
            ,TotalTackles,TacklesForLoss,Sacks,Interceptions,PassesDefended,FumblesRecovered\
            ,ForcedFumbles)
            )
        
        conn.commit()
        
        conn.close()
        
        
######################################################################### 


#Defines a function to populate data in the PlayerKickPuntReturns table. The function is called in the next section. 
def PushToKickPuntReturns(SchoolName,Year,PlayerName,KickoffReturns\
            ,KickoffReturnYds,KickoffReturnAvgYds,KickoffReturnTDs,PuntReturns,PuntReturnYds\
            ,PuntReturnAvgYds,PuntReturnTDs):
        
        conn = sqlite3.connect('CFBData.db')
        cur = conn.cursor()
    
        cur.execute('''
            INSERT INTO PlayerKickPuntReturns(SchoolName,Year,PlayerName,KickoffReturns
            ,KickoffReturnYds,KickoffReturnAvgYds,KickoffReturnTDs,PuntReturns,PuntReturnYds
            ,PuntReturnAvgYds,PuntReturnTDs)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (SchoolName,Year,PlayerName,KickoffReturns\
            ,KickoffReturnYds,KickoffReturnAvgYds,KickoffReturnTDs,PuntReturns,PuntReturnYds\
            ,PuntReturnAvgYds,PuntReturnTDs)
            )
        
        conn.commit()
        
        conn.close()
        
        
######################################################################### 


#Defines a function to populate data in the PlayerKickingPunting table. The function is called in the next section. 
def PushToKickingPunting(SchoolName,Year,PlayerName,ExtraPointsMade\
            ,ExtraPointsAttempted,ExtraPointsPct,FieldGoalsMade,FieldGoalsAttempted\
            ,FieldGoalsPct,Punts,PuntsYds,PuntsAvgYds):
        
        conn = sqlite3.connect('CFBData.db')
        cur = conn.cursor()
    
        cur.execute('''
            INSERT INTO PlayerKickingPunting(SchoolName,Year,PlayerName,ExtraPointsMade
            ,ExtraPointsAttempted,ExtraPointsPct,FieldGoalsMade,FieldGoalsAttempted
            ,FieldGoalsPct,Punts,PuntsYds,PuntsAvgYds)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (SchoolName,Year,PlayerName,ExtraPointsMade\
            ,ExtraPointsAttempted,ExtraPointsPct,FieldGoalsMade,FieldGoalsAttempted\
            ,FieldGoalsPct,Punts,PuntsYds,PuntsAvgYds)
            )
        
        conn.commit()
        
        conn.close()
        
        
######################################################################### 

def RegexParser(statText, tag):

        parseThisString = 'data-stat="'+statText+'" >.+?<'
        regexVariable = re.findall(parseThisString,str(tag))
        regexVariable = re.sub("></td><", ">0<", str(regexVariable))
        regexVariable = re.findall('>.+?<', str(regexVariable))
        return regexVariable

        
############################################################################


#This section iterates through weblinks using the school list above which contain player data
#and populates the player data in the database     
print ('Populating the Player tables. This may take several hours.')
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
        
       
        collegeStatsTags = collegeStatsSoup('div', id="all_passing")
        x = 0
        
        for tag in collegeStatsTags:
            
            PlayerName = re.findall('data-stat="player" csk=".+?"',str(tag))
            PlayerName = re.findall('"[A-Z]+.+?"', str(PlayerName))
            i = len(PlayerName)
             
            PassingCompletions = RegexParser('pass_cmp', str(tag))            
            PassingAtmpts = RegexParser('pass_att', str(tag))            
            PassingCompletePct = RegexParser('pass_cmp_pct', str(tag))            
            PassingTotYds = RegexParser('pass_yds', str(tag))            
            PassingYardsPerAttmpt = RegexParser('pass_yds_per_att', str(tag))            
            PassingTDs = RegexParser('pass_td', str(tag))            
            PassingINTs = RegexParser('pass_int', str(tag))                       
            PasserRating = RegexParser('pass_rating', str(tag))        
            
            while (x <= i-1):
                PushToPassing(collegeName,year,str(PlayerName[x])[1:-1],str(PassingCompletions[x])[1:-1]\
                ,str(PassingAtmpts[x])[1:-1],str(PassingCompletePct[x])[1:-1],str(PassingTotYds[x])[1:-1]\
                ,str(PassingYardsPerAttmpt[x])[1:-1],str(PassingTDs[x])[1:-1],str(PassingINTs[x])[1:-1]\
                ,str(PasserRating[x])[1:-1])
                
                x = x + 1
            
                
        collegeStatsTags = collegeStatsSoup('div', id="all_rushing_and_receiving")
        x = 0
                    
        for tag in collegeStatsTags:
            
            PlayerName = re.findall('data-stat="player" csk=".+?"',str(tag))
            PlayerName = re.findall('"[A-Z]+.+?"', str(PlayerName))
            i = len(PlayerName)
                        
            RushingAtmpts = RegexParser('rush_att', str(tag)) 
            RushingTotYds = RegexParser('rush_yds', str(tag))
            RushingAvgYds = RegexParser('rush_yds_per_att', str(tag))
            RushingTDs = RegexParser('rush_td', str(tag))
            Receptions = RegexParser('rec', str(tag))
            ReceivingTotYds = RegexParser('rec_yds', str(tag))
            ReceivingAvgYds = RegexParser('rec_yds_per_rec', str(tag))
            ReceivingTDs = RegexParser('rec_td', str(tag))


            while (x <= i-1):   
                PushToRushingReceiving(collegeName,year,str(PlayerName[x])[1:-1],str(RushingAtmpts[x])[1:-1]\
                ,str(RushingTotYds[x])[1:-1],str(RushingAvgYds[x])[1:-1],str(RushingTDs[x])[1:-1],str(Receptions[x])[1:-1]\
                ,str(ReceivingTotYds[x])[1:-1],str(ReceivingAvgYds[x])[1:-1],str(ReceivingTDs[x])[1:-1])
                
                x = x + 1
                
                
        collegeStatsTags = collegeStatsSoup('div', id="all_defense_and_fumbles")
        x = 0
        
        for tag in collegeStatsTags:
            
            PlayerName = re.findall('data-stat="player" csk=".+?"',str(tag))
            PlayerName = re.findall('"[A-Z]+.+?"', str(PlayerName))
            i = len(PlayerName)
            
            SoloTackles = RegexParser('tackles_solo', str(tag)) 
            AssistedTackles = RegexParser('tackles_assists', str(tag)) 
            TotalTackles = RegexParser('tackles_total', str(tag)) 
            TacklesForLoss = RegexParser('tackles_loss', str(tag)) 
            Sacks = RegexParser('sacks', str(tag)) 
            Interceptions = RegexParser('def_int', str(tag)) 
            PassesDefended = RegexParser('pass_defended', str(tag)) 
            FumblesRecovered = RegexParser('fumbles_rec', str(tag)) 
            ForcedFumbles = RegexParser('fumbles_forced', str(tag)) 
            
            while (x <= i-1):    
                PushToDefense(collegeName,year,str(PlayerName[x])[1:-1],str(SoloTackles[x])[1:-1]\
                ,str(AssistedTackles[x])[1:-1],str(TotalTackles[x])[1:-1],str(TacklesForLoss[x])[1:-1]\
                ,str(Sacks[x])[1:-1],str(Interceptions[x])[1:-1],str(PassesDefended[x])[1:-1]\
                ,str(FumblesRecovered[x])[1:-1],str(ForcedFumbles[x])[1:-1])
                
                x = x+ 1
                
                
        collegeStatsTags = collegeStatsSoup('div', id="all_returns")
        x = 0
        
        for tag in collegeStatsTags:
            
            PlayerName = re.findall('data-stat="player" csk=".+?"',str(tag))
            PlayerName = re.findall('"[A-Z]+.+?"', str(PlayerName))
            i = len(PlayerName)
        
            KickoffReturns = RegexParser('kick_ret', str(tag)) 
            KickoffReturnYds = RegexParser('kick_ret_yds', str(tag)) 
            KickoffReturnAvgYds = RegexParser('kick_ret_yds_per_ret', str(tag)) 
            KickoffReturnTDs = RegexParser('kick_ret_td', str(tag)) 
            PuntReturns = RegexParser('punt_ret', str(tag)) 
            PuntReturnYds = RegexParser('punt_ret_yds', str(tag)) 
            PuntReturnAvgYds = RegexParser('punt_ret_yds_per_ret', str(tag)) 
            PuntReturnTDs = RegexParser('punt_ret_td', str(tag)) 
                      
            while (x <= i-1):     
                PushToKickPuntReturns(collegeName,year,str(PlayerName[x])[1:-1],str(KickoffReturns[x])[1:-1]\
                ,str(KickoffReturnYds[x])[1:-1],str(KickoffReturnAvgYds[x])[1:-1],str(KickoffReturnTDs[x])[1:-1]\
                ,str(PuntReturns[x])[1:-1],str(PuntReturnYds[x])[1:-1],str(PuntReturnAvgYds[x])[1:-1]\
                ,str(PuntReturnTDs[x])[1:-1])
                
                x = x + 1
                
                
        collegeStatsTags = collegeStatsSoup('div', id="all_kicking_and_punting")
        x = 0
        
        for tag in collegeStatsTags:

            PlayerName = re.findall('data-stat="player" csk=".+?"',str(tag))
            PlayerName = re.findall('"[A-Z]+.+?"', str(PlayerName))
            i = len(PlayerName)
            
            ExtraPointsMade = RegexParser('xpm', str(tag)) 
            ExtraPointsAttempted = RegexParser('xpa', str(tag)) 
            ExtraPointsPct = RegexParser('xp_pct', str(tag)) 
            FieldGoalsMade = RegexParser('fgm', str(tag)) 
            FieldGoalsAttempted = RegexParser('fga', str(tag)) 
            FieldGoalsPct = RegexParser('fg_pct', str(tag)) 
            Punts = RegexParser('punt', str(tag)) 
            PuntsYds = RegexParser('punt_yds', str(tag)) 
            PuntsAvgYds = RegexParser('punt_yds_per_punt', str(tag)) 
                
            while (x <= i-1):  
                PushToKickingPunting(collegeName,year,str(PlayerName[x])[1:-1],str(ExtraPointsMade[x])[1:-1]\
                ,str(ExtraPointsAttempted[x])[1:-1],str(ExtraPointsPct[x])[1:-1],str(FieldGoalsMade[x])[1:-1]\
                ,str(FieldGoalsAttempted[x])[1:-1],str(FieldGoalsPct[x])[1:-1],str(Punts[x])[1:-1]\
                ,str(PuntsYds[x])[1:-1],str(PuntsAvgYds[x])[1:-1])
                
                x = x + 1
                
                
        year = year + 1
        
print ("Player tables have been populated")

print (time.asctime(time.localtime(time.time())))