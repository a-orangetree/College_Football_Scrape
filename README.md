##INTRODUCTION

This program scrapes college football data (FBS schools only) for the past 10 years from http://www.sports-reference.com. Several  cuts of data are produced and then stored in an SQLite database. The motivation behind scraping the data to practice statistics and other analytical methods (using Python, of course). 

10 years is an arbitrary number and can be of course changed. The code does take some time to run (i.e. several hours).

I will continue to improve the performance of the script and potentially add more data as time permits. Of course, as the webiste changes its layout information will change, possibly making new information available or previous displayed information unavailable. 

I am currently working on bringing in individual game statistics.

The attached CFBData DB is a sample database showes the tables and data to be expected. 


##REQUIREMENTS

Python 3 is required, along with several libraries, all of which comes standard in Continuum's Anaconda Python distrbution (found here: https://www.continuum.io/downloads).

SQLite is recommended, though not required (found here: http://sqlitebrowser.org/). All the data can be accessed using Python. However, using SQLite Browser may make some manipulations easier. Also, at any point during the scrape, you can open up the DB Browser and view the data which has been written.


##EXPLANATION OF TABLE OUTPUTS IN SQLITE

Various scripts create/update tables in an SQLite DB. What information is populated on each table and which query is responsible for populating that particular table.

###Coach Table
This table provides a yearly summary of each school's head coach. If the coach was not retained throughout the entire season, that given year will be duplicated and each coach will have a separate row.

**Columns**: SchoolName, Year, Coach

**Source Script:** PushToTeamSplits.py script

###Conference Table
This table provides a yearly summary of each school's conference. Because schools do not change conference mid-season, there should be no concern any school has multiple conference values in a given year. 

**Columns**: SchoolName, Year, Conference

**Source Script:** PushToTeamSplits.py script

###SeasonResults Table
This table provides outcome statistics of each game a school played in a given year.

**Columns**: SchoolName, Year, GameOfYear, Date, Time, Day, HomeOrAway, Opponent, Outcome, PointsFor, PointsAgainst, Wins, Losses, Streak

**Source Script:** PushToSeasonResults.py

###TeamSplits Table
This table provides summary statistics of each school's performance in a given year broken down first by Offense and Defense and then further by Home, Road, Win, Loss.

**Columns:** SchoolName, Year, Side, Value, GamesPlayed, Wins, Losses, PassCompletions, PassAtmpts, PassCompletionPct, TotalPassYds, PassTDs, TotalPlays, TotalYds, AvgYdsPerPlay, FirstDownsByPass, FirstDownsByRush, FirstDownsByPenalty, TotalFirstDowns, PenaltiesNumber, PenaltiesYds, TurnoversByFumble, TurnoversByInt, TotalTurnovers 

**Source Script:** PushToTeamSplits.py

###TeamStatistics Table
This table provides summary statistics of each school's performance in a given year broken out by Offense and Defense. Compared to the TeamSplits table, this table provides a higher level of aggregation.

**Columns**: SchoolName, Year, Side, GamesPlayed, PassingCompletions, PassingAtmpts, PassingCompletePct, PassingTotYds,PassingTDs, RushingAtmpts, RushingTotYds, RushingAvgYds, RushingTDs, TotalOffensePlays, TotalOffenseTotYds, TotalOffenseAvgYds, FirstDownsByPassing, FirstDownsByRushing, FirstDownsByPenalty, FirstDownsTot, PenaltiesTot, PenaltiesYds, TurnoversByFumble, TurnoversByInt, TurnoversTot

**Source Script:** PushToTeamYearStats.py


##KNOWN BUGS

* TeamSplits table is currently not populating the Wins and Losses columns for games played at a Neutral site.


