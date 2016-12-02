##INTRODUCTION

This program scrapes college football data (FBS schools only) for the past 10 years from http://www.sports-reference.com. Several  cuts of data are produced and then stored in an SQLite database. The motivation behind scraping the data to practice statistics and other analytical methods (using Python, of course). 

10 years is an arbitrary number and can be changed. Some portions of the code are inefficient and [occassionally] timeout.


##REQUIREMENTS

Python 3 is required, along with several libraries, all of which comes standard in Continuum's Anaconda Python distrbution (found here: https://www.continuum.io/downloads).

SQLite is recommended, though not required (found here: http://sqlitebrowser.org/). All the data can be accessed using Python. However, using SQLite Browser may make some manipulations easier.


##EXPLANATION OF TABLE OUTPUTS IN SQLITE

Various scripts create/update tables in an SQLite DB. What information is populated on each table and which query is responsible for populating that particular table.

###COACH
This table provides a yearly summary of each school's head coach. If the coach was not retained throughout the entire season, that given year will be duplicated and each coach will have a separate row.

This table is populated by running the PushToTeamSplits.py script.

###CONFERENCE
This table provides a yearly summary of each school's conference. Because schools do not change conference mid-season, there should be no concern any school has multiple conference values in a given year. 

This table is populated by running the PushToTeamSplits.py script.

###GAME RESULTS
This table provides statistics for each game a school played over the period of time indicated.

This table is populated by running the AutoRunPushToGameResults.py script. This script calls the PushToGameResultsTest2 script. Prior to this table being populated, you *must* populate the SeasonResults table.

###SEASON RESULTS
This table provides outcome statistics of each game a school played in a given year.

This table is populated by running the PushToSeasonResults.py script.

###TEAM SPLITS
This table provides summary statistics of each school's performance in a given year broken down first by Offense and Defense and then further by Home, Road, Win, Loss.

This table is populated by running the PushToTeamSplits.py script.

###TEAM STATISTICS
This table provides summary statistics of each school's performance in a given year broken out by Offense and Defense. Compared to the TEAM SPLITS table, this table provides a higher level of aggregation.

This table is populated by running the PushToTeamYearStats.py script.


