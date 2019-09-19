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
    print()
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
    print()


def main():
    
    schools = get_schools()
    push_schools(schools)
    return schools
        


