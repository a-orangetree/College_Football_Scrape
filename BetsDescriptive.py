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

#
#dfGameSeason = pandas.merge(dfGame, dfSeason, how='inner', on=['SchoolName','Date'])
#
#print (dfGameSeason.describe())
#print (dfGameSeason.head(10))

dfSplits['Wins'] = pandas.to_numeric(dfSplits['Wins'])
dfSplits['Losses'] = pandas.to_numeric(dfSplits['Losses'])

dfSplits['Side'] = dfSplits['Side'].astype('category')
dfSplits['Value'] = dfSplits['Value'].astype('category')

dfSplits = pandas.merge(dfSplits, dfConference, how = 'left', on = ['SchoolName','Year'])
dfSplits['Conference'] = dfSplits['Conference'].astype('category')

###############################################
sea.set_style('whitegrid')
sea.set_context('talk')
#plt.figure(figsize=(11,10))

dfWinSplits = dfSplits[(dfSplits['Value'] == 'Win')]
dfOffensiveWinSplits = dfSplits[(dfSplits['Value'] == 'Win') & (dfSplits['Side'] == 'Offense')]
dfDefensiveWinSplits = dfSplits[(dfSplits['Value'] == 'Win') & (dfSplits['Side'] == 'Defense')]
#dfOffensiveWinSplits.info()

def PassCompletePctBin(row):
     if (row['PassCompletionPct'] >= 80):
         return '80+'
     if (row['PassCompletionPct'] >= 70):
         return '70s'
     if (row['PassCompletionPct'] >= 60):
         return '60s'
     if (row['PassCompletionPct'] >= 50):
         return '50s'
     if (row['PassCompletionPct'] >= 40):
         return '40s'
     else: return 'Less than 40'

dfWinSplits['PassCompletePctBin'] = dfWinSplits.apply(lambda row: PassCompletePctBin (row), axis = 1)
#print (dfWinSplits['PassCompletePctBin'].value_counts())

#print (dfWinSplits.head(10))
dfWinSplits.info()

dfWinSplits['PassCompletePctBin'] = dfWinSplits['PassCompletePctBin'].astype('category')

#model1 = smf.ols(formula = 'Value ~ PassCompletionPct', data = dfWinSplits)
#
#results1 = model1.fit()
#print (results1.summary())

#####################################################################################
#sea.factorplot(x = 'Conference', y = 'PassCompletionPctBin', kind = 'box',\
# data = dfOffensiveWinSplits, size = 6, aspect = 2)
#plt.xticks(rotation = 60)

#sea.factorplot(x = 'Conference', y = 'PassCompletionPctBin', kind = 'box',\
# data = dfDefensiveWinSplits, size = 6, aspect = 2)
#plt.xticks(rotation = 60)


