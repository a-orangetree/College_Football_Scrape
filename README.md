##INTRODUCTION

This program performs a webscrape of college football data (FBS schools only) from http://www.sports-reference.com.  Several  cuts of data are produced and then stored in an SQLite database. The purpose is educational in a providing a useful, real-world webscraping example, simple database manipulation, and analysis of data using the Pandas library.

The data collected is for the past 10 years. 10 years is an arbitrary number, of course, and can be changed. The code does take some time to run (i.e. several hours).

I will continue to improve the performance of the script and potentially add more data as time permits. Websites change often however, and changes will potentially create bugs and make new information available or previously displayed information unavailable. 


##REQUIREMENTS

Python 3 is required, along with several libraries, all of which comes standard in Continuum's Anaconda Python distrbution (found here: https://www.continuum.io/downloads).

Jupyter Notebook is required to view the SampleAnalysisUsingPython&JupyterNotebook.ipynb. This package comes standard in Continuum's Anaconda Python distributon as well, or it can be downloaded separately (found here: https://jupyter.org/). Once installed, open a terminal and type: "jupyter notebook" to open the program. 

SQLite is recommended, though not required (found here: http://sqlitebrowser.org/). All the data can be accessed using Python. However, using SQLite Browser may make some manipulations easier. Also, at any point during the scrape, you can open up the DB Browser and view the data which has been written.


##EXPLANATION OF TABLE OUTPUTS IN SQLITE

Various scripts create/update tables in an SQLite DB. What information is populated on each table and which query is responsible for populating that particular table.

###Coach Table
This table provides a yearly summary of each school's head coach. If the coach was not retained throughout the entire season, that given year will be duplicated and each coach will have a separate row.

**Columns**: SchoolName, Year, Coach

**Source Script:** PushToTeamSplits.py

###Conference Table
This table provides a yearly summary of each school's conference. Because schools do not change conference mid-season, there should be no concern any school has multiple conference values in a given year. 

**Columns**: SchoolName, Year, Conference

**Source Script:** PushToTeamSplits.py

###GameResults Table
This table provides individual game statistics. This table does not have data for games played against non-FBS teams

**Columns**: SchoolName, Year, GameDate, Opponent, HomeOrAway, TotalYards, TotalRushes, RushingYards, RushingTDs, NumberOfPassingAtmpts, PassingCompletions, PassingYards, PassingTDs, PassingINTs, FirstDowns, NumberOfFumbles, LostFumbles, Turnovers, NumberOfPenalties, PenaltyYards, opponentTotalYards, opponentTotalRushes, opponentRushingYards, opponentRushingTDs,  opponentNumberOfPassingAtmpts, opponentPassingCompletions, opponentPassingYards, opponentPassingTDs, opponentPassingINTs, opponentFirstDowns, opponentNumberOfFumbles, opponentLostFumbles, opponentTurnovers, opponentNumberOfPenalties, opponentPenaltyYards

**Source Script**: PushToGameResults.py

**Note:** This table is currently not populating certain data for games played at a Neutral site.

###SeasonResults Table
This table provides outcome statistics of each game a school played in a given year.

**Columns**: SchoolName, Year, GameOfYear, Date, Time, Day, HomeOrAway, Opponent, Outcome, PointsFor, PointsAgainst, Wins, Losses, Streak

**Source Script:** PushToSeasonResults.py

###TeamSplits Table
This table provides summary statistics of each school's performance in a given year broken down first by Offense and Defense and then further by Home, Road, Win, Loss.

**Columns:** SchoolName, Year, Side, Value, GamesPlayed, Wins, Losses, PassCompletions, PassAtmpts, PassCompletionPct, TotalPassYds, PassTDs, TotalPlays, TotalYds, AvgYdsPerPlay, FirstDownsByPass, FirstDownsByRush, FirstDownsByPenalty, TotalFirstDowns, PenaltiesNumber, PenaltiesYds, TurnoversByFumble, TurnoversByInt, TotalTurnovers 

**Source Script:** PushToTeamSplits.py

**Note:** This table is currently not populating certain data for games played at a Neutral site.

###TeamStatistics Table
This table provides summary statistics of each school's performance in a given year broken out by Offense and Defense. Compared to the TeamSplits table, this table provides a higher level of aggregation.

**Columns**: SchoolName, Year, Side, GamesPlayed, PassingCompletions, PassingAtmpts, PassingCompletePct, PassingTotYds,PassingTDs, RushingAtmpts, RushingTotYds, RushingAvgYds, RushingTDs, TotalOffensePlays, TotalOffenseTotYds, TotalOffenseAvgYds, FirstDownsByPassing, FirstDownsByRushing, FirstDownsByPenalty, FirstDownsTot, PenaltiesTot, PenaltiesYds, TurnoversByFumble, TurnoversByInt, TurnoversTot

**Source Script:** PushToTeamYearStats.py

**Note:** Duplicates exist on this table. These can be filtered either in SQL using the DISTINCT keyword, or in Python using the drop_duplicates() method.


##KNOWN BUGS / TODO

* TeamSplits and GameResults tables are currently not populating certain data for games played at a Neutral site.
* GameResults does not have data for games played against non-FBS teams
* Duplicates exist on the TeamStatistics table. These can be filtered either in SQL using the DISTINCT keyword, or in Python using the drop_duplicates() method.


##OTHER FILES

* CFBData.db: sample database which shows the tables and data to be expected.
* SampleAnalysisUsingPython&JupyterNotebook.ipynb: example code constructed in Jupyter Notebook which can used as the jumping off point for analysis of the data

