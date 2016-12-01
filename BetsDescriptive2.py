import pandas
import numpy
import sqlite3
import seaborn as sea
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf

conn = sqlite3.connect('BettingData.db')
dfTeams = pandas.read_sql_query('SELECT * FROM TeamStatistics', conn)
dfSplits = pandas.read_sql_query('SELECT * FROM TeamSplits', conn)
dfConference = pandas.read_sql_query('SELECT * FROM Conference', conn)
dfCoach = pandas.read_sql_query('SELECT * FROM Coach', conn)
dfSeason = pandas.read_sql_query('SELECT * FROM SeasonResults', conn)
dfGame = pandas.read_sql_query('SELECT * FROM GameResults', conn)
##############################################################################

dfTeams['offensePassingCompletePct'] = pandas.to_numeric(dfTeams['offensePassingCompletePct'])


#dfTeams.info()
dfTeams = dfTeams[dfTeams['offensePassingCompletePct'] > 50.0]
#dfTeams = dfTeams.sort_values(['offensePassingCompletePct'], ascending=['False'])
dfTeams = dfTeams.sort_values(['totalOffenseTotYds'], ascending=['False'])
print (dfTeams)




###############################################################################
dfGameSeason = pandas.merge(dfGame, dfSeason, how='inner', on=['SchoolName','Date','Opponent'])
dfGameSeason = pandas.merge(dfGameSeason, dfConference, how='inner',on=['SchoolName','Year'])

dfGameSeason['PointsFor'] = pandas.to_numeric(dfGameSeason['PointsFor'])
dfGameSeason['PointsAgainst'] = pandas.to_numeric(dfGameSeason['PointsAgainst'])
dfGameSeason['Conference'] = dfGameSeason['Conference'].astype('category')
#dfGameSeason['Year'] = dfGameSeason['Year'].astype('category')
dfGameSeason['GameOfYear'] = dfGameSeason['GameOfYear'].astype('category')

dfGameSeason['Spread'] = dfGameSeason['PointsFor']-dfGameSeason['PointsAgainst']

def SpreadBin(row):
     if (row['Spread'] > 30):
         return '30+'
     if (row['Spread'] > 20):
         return '20+'
     if (row['Spread'] >= 10):
         return '10s'
     if (row['Spread'] >= 0):
         return '1s'
     else:
         return 'negative'

dfGameSeason['SpreadBin'] = dfGameSeason.apply(lambda row: SpreadBin (row), axis = 1)
#print (dfGameSeason['SpreadBin'].value_counts())

dfGameSeason['SpreadBin'] = dfGameSeason['SpreadBin'].astype('category')

#print (dfGameSeason.info())

#print (dfGameSeason.head(10))

###############################################
sea.set_style('whitegrid')
sea.set_context('talk')
#plt.figure(figsize=(11,10))

#sea.factorplot(x = 'GameOfYear', y = 'Spread', kind = 'bar',\
# data = dfFIU, size = 6, aspect = 2)
#plt.xticks(rotation = 60)

#sea.factorplot(x = 'Conference', y = 'PassCompletionPct', kind = 'box',\
# data = dfDefensiveWinSplits, size = 6, aspect = 2)
#plt.xticks(rotation = 60)


