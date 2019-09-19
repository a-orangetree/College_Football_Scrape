import urllib.request, sqlite3, re, datetime, sys, pandas as pd
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup

def get_year_data(college_urls):

    print('retrieving year data')
    print(datetime.datetime.now())
    
    injuries = pd.DataFrame(columns = ['SchoolName', 'Player', 'Status', 'Comment'])
    team_stats = pd.DataFrame(columns = ['SchoolName', 'Split', 'G', 'Pass_Cmp', 'Pass_Att', 'Pass_Cmp_Pct', 'Pass_Yds', 'Pass_TD', 'Rush_Att', 'Rush_Yds', 'Rush_Yds_Per_Att', 'Rush_TD', 'Tot_Plays', 'Tot_Yds', 'Tot_Yds_Per_Play', 'First_Down_Pass', 'First_Down_Rush', 'First_Down_Pen', 'First_Down_Tot', 'Penalties_Num', 'Turnovers_Yds', 'Turnovers_Fum', 'Turnsovers_Int', 'Turnovers_Tot'])

    for row in college_urls.iterrows():
        
        college = row[1]['SchoolName']
        url = row[1]['SchoolURL']
        
        print(college)
        print(url)
        
        try: 
            html = urllib.request.urlopen(url).read()
            
        except: 
            print ('collegesURL is not working:',url)
            
        colleges_soup = BeautifulSoup(html, 'html.parser')

        ############
        # INJURIES
        ############
        table_injuries = colleges_soup.find(id='injuries')
        if table_injuries is None:
            continue
        tbody = table_injuries.find('tbody')
        for tr in tbody.find_all('tr'):
            player = None
            comment = None
            status = None
            for a in tr.find_all('a'):
                player = a.text[:-2]
            for td in tr.find_all('td'):
                data_stat = td.get('data-stat')
                if data_stat == 'comment':
                    comment = td.text
                elif data_stat == 'status':
                    status = td.text
                        
        injuries = injuries.append({'SchoolName': college, 'Player': player, 'Status': status, 'Comment': comment}, ignore_index = True)
        table_injuries = None
        
        #########
        # SPLITS
        #########
        table_team = colleges_soup.find(id='team')
        if table_team is None:
            continue
        tbody = table_team.find('tbody')
        for tr in tbody.find_all('tr'):
            th = tr.find('th')
            split = th.text
            for td in tr.find_all('td'):
                data_stat = td.get('data-stat')
                if data_stat == 'g':
                    g = td.text
                elif data_stat == 'pass_cmp':
                    pass_cmp = td.text
                elif data_stat == 'pass_att':
                    pass_att = td.text
                elif data_stat == 'pass_cmp_pct':
                    pass_cmp_pct = td.text
                elif data_stat == 'pass_yds':
                    pass_yds = td.text
                elif data_stat == 'pass_td':
                    pass_td = td.text
                elif data_stat == 'rush_att':
                    rush_att = td.text
                elif data_stat == 'rush_yds':
                    rush_yds = td.text
                elif data_stat == 'rush_yds_per_att':
                    rush_yds_per_att = td.text
                elif data_stat == 'rush_td':
                    rush_td = td.text
                elif data_stat == 'tot_plays':
                    tot_plays = td.text
                elif data_stat == 'tot_yds':
                    tot_yds = td.text
                elif data_stat == 'tot_yds_per_play':
                    tot_yds_per_play = td.text
                elif data_stat == 'first_down_pass':
                    first_down_pass = td.text
                elif data_stat == 'first_down_rush':
                    first_down_rush = td.text
                elif data_stat == 'first_down_penalty':
                    first_down_penalty = td.text
                elif data_stat == 'first_down':
                    first_down = td.text
                elif data_stat == 'penalty':
                    penalty = td.text
                elif data_stat == 'penalty_yds':
                    penalty_yds = td.text
                elif data_stat == 'fumbles_lost':
                    fumbles_lost = td.text
                elif data_stat == 'pass_int':
                    pass_int = td.text
                elif data_stat == 'turnovers':
                    turnovers = td.text
    
            team_stats = team_stats.append({'SchoolName':college, 'Split':split, 'G':g, 'Pass_Cmp':pass_cmp, 'Pass_Att':pass_att, 'Pass_Cmp_Pct':pass_cmp_pct, 'Pass_Yds':pass_yds, 'Pass_TD':pass_td, 'Rush_Att':rush_att, 'Rush_Yds':rush_yds, 'Rush_Yds_Per_Att':rush_yds_per_att, 'Rush_TD':rush_td, 'Tot_Plays':tot_plays, 'Tot_Yds':tot_yds, 'Tot_Yds_Per_Play':tot_yds_per_play, 'First_Down_Pass':first_down_pass, 'First_Down_Rush':first_down_rush, 'First_Down_Pen':first_down_penalty, 'First_Down_Tot':first_down, 'Penalties_Num':penalty, 'Turnovers_Yds':penalty_yds, 'Turnovers_Fum':fumbles_lost, 'Turnsovers_Int':pass_int, 'Turnovers_Tot':turnovers}, ignore_index = True)
        
        table_team = None

    print(datetime.datetime.now())
    print()
    return (injuries, team_stats)
    
    
def push_year_data(injuries, team_stats):
    
    conn = sqlite3.connect('CFBData.db')
    cur = conn.cursor()

    print('writing injuries to the database')
    print(datetime.datetime.now())
    cur.executescript('DROP TABLE IF EXISTS Injuries;')
    injuries.to_sql('Injuries', conn)
    
    print('writing team stats to the database')
    print(datetime.datetime.now())
    cur.executescript('DROP TABLE IF EXISTS Team_Stats;')
    team_stats.to_sql('Team_Stats', conn)

    conn.close()
    print(datetime.datetime.now())
    print()
    
    
    
def main(schools):
    
    data = get_year_data(schools)
    injuries = data[0]
    team_stats = data[1]
    push_year_data(injuries, team_stats)