## Sequential Scraping
from bs4 import BeautifulSoup
import pandas as pd
import time, requests, argparse, json
from typing import List, Dict, Union, Optional
from config import CONFIG
import logging
from logs import log
from color_scheme import bcolors

titles = 'data scientist, data analyst, machine learning engineer, software engineer, data analyst, data engineer'
class ParseKwargs(argparse.Action):
    """Allow inputs to be passes like dictionary in parser"""
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, dict())
        for value in values:
            key, value = value.split('=')
            getattr(namespace, self.dest)[key] = value

def get_args():
    parser = argparse.ArgumentParser('fill module funcs here', add_help=True)
    parser.add_argument('--LOGLVL','-loglvl', type=str, default='warning',
                        help='log level')
    parser.add_argument('--LOG_PATH', '-logp', type=str, default='./',
                        help='path to save log file')
    parser.add_argument('--LOG_FILENAME', '-logfname', type=str, default='logs.log',
                        help='name of log file')
    parser.add_argument('--LOCATIONS', '-locs', type=str, default='''Houston, TX, Dallas, TX, Dallas-Fort Worth, TX, San Francisco, CA, New York, NY, Philadelphia, PA, Pittsburgh, PA, Boston, MA, Washington, DC''', 
                        help='cities and states to crawl seperated by comma (format defined by Indeed l paramter')
    parser.add_argument('--PAGE', '-pg', type=int, default=10,
                        help='number of pages to crawl for each query')
    parser.add_argument('--PARAMS', '-q', action=ParseKwargs, nargs='*',
                        help='parameters to pass to query')
    parser.add_argument('--TITLES', '-t', type=str, default=titles)
    # parser.add_argument('-k', '--kwargs', nargs='*', action=ParseKwargs)
    return parser


class Crawler():
    """Job Posts crawler from Indeed"""
    def __init__(self, logger:logging.RootLogger) -> None:
        self.logger = logger

    def getInfo(self, div:BeautifulSoup) -> Dict:
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


    def getJobPost(self, URL:str='http://www.indeed.com/jobs?', queries:Optional[dict]=None) -> BeautifulSoup:
        """[Get list of job postings from indeed]

        Keyword Arguments:
            URL {str} -- [Can be modified to scrape from other sites]
            (default: {'http://www.indeed.com/jobs?'})
            queries {dict} -- [queries to scrape] (default: {None})

        Returns:
            BeautifulSoup -- [description]
        """
        divs = None
        try:
            page = requests.get(URL, params=queries)
        except Exception as e:
            self.logger.debug(f"Server's response: {page.status_code}")
            self.logger.error(e)
        else:
            if page == None:
                self.logger.error('Not found page')
            else:
                soup = BeautifulSoup(page.text, 'html.parser')
                divs = soup.find_all(name='div', attrs={'data-tn-component': 'organicJob'})
        return divs

    def get_jobdes(self, summary_links:List[str], base_web:str='https://www.indeed.com') -> List[str]:
        """[Get job descriptions from Indeed]

        Args:
            summary_links (List[str]): [list of connecting links]
            base_web (str, optional): [base linke]. Defaults to 'https://www.indeed.com'.

        Returns:
            List[str]: [Return a list-like of jobdescriptions for each link provided]
        """        
        summaries = []
        try:
            for tail in summary_links:
                link = base_web + tail
                page = requests.get(link)
                soup = BeautifulSoup(page.text, 'html.parser')
                div = soup.find_all('div', attrs={'id': 'jobDescriptionText'})
                summaries.append([link, div[0].text])
        except IndexError:
            self.logger.error('Here\'s what div looks like\n:', div)
            self.logger.error('URL:', link)
        return pd.DataFrame(summaries, columns = ['links', 'description'])




# Main 
def main(args):
    logger = log(path=str(CONFIG.log_path), filename=args.LOG_FILENAME, level=args.LOGLVL)
    logger.debug(type(logger))
    start = time.time()
    crawler = Crawler(logger=logger)
    no_jobs = 0
    start_page = 0  # one input argument
    end_page = 10  # one input argument
    JobInfo = []
    # locations = ['Houston, TX', 'Dallas, TX', 'Dallas-Fort Worth, TX', 'San Francisco, CA',
    #             'New York, NY', 'Philadelphia, PA', 'Pittsburgh, PA', 'Boston, MA', 'Washington, DC']
    loc_temp = args.LOCATIONS
    loc_temp = loc_temp.split(',')
    loc_temp = [x.strip() for x in loc_temp]
    i = 0
    locations = []
    while i < len(loc_temp) - 2:
        city = loc_temp[i]
        state = loc_temp[i+1]
        city_state = city + ', ' + state
        locations.append(city_state)
        i += 2
    params = {'q': 'data scientist', 'l': 'Houston, TX', 'explvl': 'entry_level', 'jt': 'fulltime', 'start': 0}
    if args.PARAMS is not None:
        for key, val in args.PARAMS.items():
            params[key] = val
    titles = args.TITLES.split(',')
    logger.info(f'''
    \t- {bcolors.BOLD}{bcolors.UNDERLINE}Locations to crawl{bcolors.ENDC}: {bcolors.OKGREEN}{locations}{bcolors.ENDC}\n 
    \t- {bcolors.BOLD}{bcolors.UNDERLINE}Number of Pages to crawl per query{bcolors.ENDC}: {bcolors.OKGREEN}{args.PAGE}{bcolors.ENDC}\n 
    \t- {bcolors.BOLD}{bcolors.UNDERLINE}Queries parameters{bcolors.ENDC}: {bcolors.OKGREEN}{params}{bcolors.ENDC}\n
    \t- {bcolors.BOLD}{bcolors.UNDERLINE}Job titles{bcolors.ENDC}: {bcolors.OKGREEN}{titles}{bcolors.ENDC}''')



    # URL = 'https://www.indeed.com/jobs?q=Data+Scientist&l=Texas&explvl=entry_level'

    print('\t- Starting Crawling ...')
    # TODO: Fix crawler to scrape from all locations instead of just TX
# # TODO: Parallelizing web scraping
    for l in locations:
        for t in titles:
            for page in range(start_page, end_page):
                params['q'] = t
                params['l'] = l
                params['start'] = page * no_jobs
                logger.info(' Getting information from the provided URL...')
                divs = crawler.getJobPost(queries=params)
                no_jobss = len(divs)
                logger.info(f' The number of job postings found is {no_jobss}')
                for div in divs:
                    temp_info = crawler.getInfo(div)
                    JobInfo.append(temp_info)
                no_jobs = no_jobss
                logger.info(f" Done scraping for position {params['q']} at {params['l']}, job number from {params['start']}")
                logger.info(f" Continue with next query")
    data = pd.DataFrame(JobInfo)
    data = data.drop_duplicates()
    logger.critical(f'Saving raw data to {str(CONFIG.data_path / "raw")}...')
    data.to_csv(str(CONFIG.data_path / 'raw') + '/jobpostsRaw.csv', index=False)
    time.sleep(1)
    logger.info("Done scraping from Indeed!")
    logger.critical(f'{bcolors.BOLD}{bcolors.GREEN}{bcolors.UNDERLINE}It takes {(time.time() - start) / 60: .2f} minutes for execution{bcolors.ENDC}')

if __name__ == "__main__":
    parser = get_args()
    args = parser.parse_args()
    main(args)

