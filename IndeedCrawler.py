## Sequential Scraping
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from typing import List, Dict,


def getInfo(div: BeautifulSoup) -> Dict:
    '''Take input as a bs4 tag and return a dict with information about
    a job posting
    Input
    -----
    div: list-like
        a bs4 tag of job posting
    Output
    ------
        return a dictionary with information about job title, summary link to job description,
        job location, company name'''
    temp_info = {}
    for a in div.find_all('a', attrs={'data-tn-element': 'jobTitle'}):
        temp_info['title'] = a.text
        temp_info['summarylinks'] = a['href']
    for name in div.find_all('span', attrs={'class': 'company'}):
        temp_info['name'] = name.text
    for loc in div.find_all('span', attrs={'class': 'location accessible-contrast-color-location'}):
        temp_info['location'] = loc.text
    return temp_info


def getJobPost(URL: str = 'http://www.indeed.com/jobs?', queries: dict = None) -> BeautifulSoup:
    """[Get list of job postings from indeed]

    Keyword Arguments:
        URL {str} -- [Can be modified to scrape from other sites]
        (default: {'http://www.indeed.com/jobs?'})
        queries {dict} -- [queries to scrape] (default: {None})

    Returns:
        BeautifulSoup -- [description]
    """
    try:
        page = requests.get(URL, params=queries)
    except Exception as e:
        print(e)
    else:
        if page == None:
            print('Not found page')
        else:
            soup = BeautifulSoup(page.text, 'html.parser')
    divs = soup.find_all(name='div', attrs={'data-tn-component': 'organicJob'})
    return divs

def get_jobdes(summary_links: List[str], base_web='https://www.indeed.com') -> List[str]:
    """Get job descriptions from Indeed
    Input:
    -----
    summary_links: list-like
        list of connecting links
    base_web: www.indeed.com
    Output:
    -----
        Return a list-like of jobdescriptions for each link provided"""
    summaries = []
    try:
        for tail in summary_links:
            link = base_web + tail
            page = requests.get(link)
            soup = BeautifulSoup(page.text, 'html.parser')
            div = soup.find_all('div', attrs={'id': 'jobDescriptionText'})
            summaries.append([link, div[0].text])
    except IndexError:
        print('Here\'s what div looks like\n:', div)
        print('URL:', link)
    return pd.DataFrame(summaries, columns = ['links', 'description'])

##
start = time.time()
no_jobs = 14
start_page = 0  # one input argument
end_page = 10  # one input argument
JobInfo = []
locations = ['Houston, TX', 'Dallas, TX', 'Dallas-Fort Worth, TX', 'San Francisco, CA',
             'New York, NY', 'Philadelphia, PA', 'Pittsburgh, PA', 'Boston, MA', 'Washington, DC']

titles = ['data scientist', 'data analyst', 'machine learning engineer', 'software engineer', 'data analyst','data engineer']
params = {'q': 'data scientist', 'l': 'Houston, TX', 'explvl': 'entry_level', 'jt': 'fulltime', 'start': 0}
# URL = 'https://www.indeed.com/jobs?q=Data+Scientist&l=Texas&explvl=entry_level'

for l in locations:
    for t in titles:
        for page in range(start_page, end_page):
            params['q'] = t
            params['l'] = l
            params['start'] = page * no_jobs
            print('[INFO] Getting information from the provided URL...')
            divs = getJobPost(queries=params)
            no_jobss = len(divs)
            print(f'[INFO] THe number of job postings found is {no_jobss}')
            for div in divs:
                temp_info = getInfo(div)
                JobInfo.append(temp_info)
            no_jobs = no_jobss
            print(f"[INFO] Done scraping for position {params['q']} at {params['l']}, job number from {params['start']}")
            print(f"[INFO] Continue with next query")
data = pd.DataFrame(JobInfo)
data = data.drop_duplicates()
print("[INFO] Done scraping from Indeed")


