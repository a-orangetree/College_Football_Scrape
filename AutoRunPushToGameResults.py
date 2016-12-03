import PushToGameResults
import time
import sqlite3


print (time.asctime(time.localtime(time.time())))


conn = sqlite3.connect('CFBData.db')
cur = conn.cursor()

cur.executescript('''

DROP TABLE IF EXISTS GameResults;

CREATE TABLE GameResults (
    SchoolName TEXT
    ,Date TEXT
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

print ('GameResults table Created')

conn.close()


x = 0
    

while x < 1000:
    print ('Running')
    PushToGameResults.myMainFunction()
    x = x + 1
    print ('Sleeping')
    time.sleep(30)
    