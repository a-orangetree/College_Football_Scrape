import urllib.request, sqlite3, re, datetime, sys, pandas as pd
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup

def get_schools():
    
    print('retrieving schools')
    print(datetime.datetime.now())
    
    college_urls = pd.DataFrame(columns = ['SchoolName', 'SchoolURL'])

    current_year = datetime.datetime.now().year
    standings_url = 'https://www.sports-reference.com/cfb/years/{}-standings.html'.format(current_year)

    try: html = urllib.request.urlopen(standings_url).read()
    except: print('collegesURL is not working:',standings_url)

    colleges_soup = BeautifulSoup(html, 'html.parser')
    colleges_tags = colleges_soup('a')

    for tag in colleges_tags:
        if re.search('.+/cfb/schools/.+', str(tag)):
            school_name_re = re.compile('/schools/(.+)/2')
            school_name = re.findall(school_name_re, str(tag))
            if school_name:
                school_name = school_name.pop()
                school_url = 'https://www.sports-reference.com/cfb/schools/{}/{}.html'.format(school_name, current_year)
                
                college_urls = college_urls.append({'SchoolName': school_name, 'SchoolURL': school_url}, ignore_index=True)
        else: continue
            
    college_urls = college_urls.drop_duplicates()
    print(datetime.datetime.now())
    return college_urls
    
    
def push_schools(schools):
    
    print('writing schools to the database')
    print(datetime.datetime.now())
    
    conn = sqlite3.connect('CFBData.db')
    cur = conn.cursor()

    cur.executescript('DROP TABLE IF EXISTS Schools;')
    schools.to_sql('Schools', conn)

    conn.close()
    print(datetime.datetime.now())
    
    
def get_current_year_injuries(college_urls):

    print('retrieving injuries')
    print(datetime.datetime.now())
    
    injuries = pd.DataFrame(columns = ['school', 'player', 'status', 'comment'])
    
    def _get_current_year_injuries(row):
        
        college = row['SchoolName']
        url = row['SchoolURL']
        
        try: html = urllib.request.urlopen(url).read()
        except: print ('collegesURL is not working:',url)
            
        colleges_soup = BeautifulSoup(html, 'html.parser')
        colleges_tags = colleges_soup('table')

        for table in colleges_soup.find_all('table', {'id':'injuries'}):
            if table is None:
                break
            tbody = table.find('tbody')
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
                        
            return {'school': college, 'player': player, 'status': status, 'comment': comment}
    
    injuries = injuries.append(college_urls.apply(lambda x: _get_current_year_injuries(x), axis=1), ignore_index = True)

    print(datetime.datetime.now())
    return injuries
    
    
def push_injuries(injuries):
    
    conn = sqlite3.connect('CFBData.db')
    cur = conn.cursor()

    cur.executescript('DROP TABLE IF EXISTS Injuries;')
    injuries.to_sql('Injuries', conn)

    conn.close()


def main():
    
    schools = get_schools()
    push_schools(schools)
    
    injuries = get_current_year_injuries(schools)
    push_injuries(injuries)
    
main()
        


