## Sequential Scraping
from logging import log
from bs4 import BeautifulSoup
import pandas as pd
import time, requests, argparse, json
from typing import List, Dict, Union, Optional

from proxyManager import ProxyManager
from Crawler import Crawler
from config import CONFIG
import logging
from logzero import setup_logger

titles = 'data scientist, data analyst, machine learning engineer, software engineer, data analyst, data engineer'
loglv = {'info': logging.INFO, 'warning': logging.WARNING, 'debug': logging.DEBUG, 'critical': logging.CRITICAL}
class ParseKwargs(argparse.Action):
    """Allow inputs to be passes like dictionary in parser"""
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, dict())
        for value in values:
            key, value = value.split('=')
            getattr(namespace, self.dest)[key] = value

def get_args():
    parser = argparse.ArgumentParser('fill module funcs here', add_help=True)
    parser.add_argument('--LOGLVL','-loglvl', type=str, default='info',
                        help='log level')
    parser.add_argument('--LOCATIONS', '-locs', type=str, default='''Houston, TX, Dallas, TX, Dallas-Fort Worth, TX, San Francisco, CA, New York, NY, Philadelphia, PA, Pittsburgh, PA, Boston, MA, Washington, DC''', 
                        help='cities and states to crawl seperated by comma (format defined by Indeed l paramter')
    parser.add_argument('--PAGE', '-pg', type=int, default=10,
                        help='number of pages to crawl for each query')
    parser.add_argument('--PARAMS', '-q', action=ParseKwargs, nargs='*',
                        help='parameters to pass to query')
    parser.add_argument('--TITLES', '-t', type=str, default=titles)
    # parser.add_argument('-k', '--kwargs', nargs='*', action=ParseKwargs)
    return parser

# TODO: handle case when there are no more job posts
class NojobError(Exception):
    pass

# Main 
def main(args):
    logger = setup_logger(name=__file__, logfile=CONFIG.log_path / 'seq_indeed.log', level=loglv[args.LOGLVL])
    logger.debug(type(logger))
    start = time.time()
    # Initiate Indeed crawler
    crawler = Crawler()
    no_jobs = 0
    start_page = 0  # one input argument
    end_page = 10  # one input argument
    JobInfo = []
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
    logger.debug(f"Locations to scrape {loc_temp}.")
    params = {'q': 'data scientist', 'l': 'Houston, TX', 'explvl': 'entry_level', 'jt': 'fulltime', 'start': 0}
    if args.PARAMS is not None:
        for key, val in args.PARAMS.items():
            params[key] = val
    titles = args.TITLES.split(',')
    logger.info(f'''
    \t- Locations to crawl: {locations}\n 
    \t- Number of Pages to crawl per query: {args.PAGE}\n 
    \t- Queries parameters: {params}\n
    \t- Job titles: {titles}''')

    print('\t- Starting Crawling ...')
# # TODO: Parallelizing web scraping
    for l in locations:
        proxy_scraper = ProxyManager()
        proxy_scraper.update_proxy_list()
        for t in titles:
            for page in range(start_page, end_page):
                proxy = proxy_scraper.get_proxy()
                params['q'] = t
                params['l'] = l
                params['start'] = page * no_jobs
                logger.info(' Getting information from the provided URL...')
                logger.debug(f"queue with {params}...")
                divs = crawler.getJobPost(queries=params, proxy=proxy)
                if divs is not None:
                    no_jobs = len(divs)
                elif divs is None:
                    logger.info("No more jobs to scrape!")
                    continue
                logger.info(f' The number of job postings found is {no_jobs}')
                for div in divs:
                    temp_info = crawler.getInfo(div)
                    # TODO: Insert codes to retrieve job des and loc here
                    temp_info['location'] = params['l']
                    JobInfo.append(temp_info)
                # TODO: Fix code to use database instead of csv file
                # TODO: Ensure that if there are no jobs, crawler escape loop
                logger.info(f" Done scraping for position {params['q']} at {params['l']}, job number from {params['start']}")
                logger.info(f" Continue with next query")
    data = pd.DataFrame(JobInfo)
    data = data.drop_duplicates()
    logger.critical(f'Saving raw data to {str(CONFIG.data_path / "raw")}...')
    data.to_csv(str(CONFIG.data_path / 'raw') + '/jobpostsRaw.csv', index=False)
    time.sleep(1)
    logger.info("Done scraping from Indeed!")
    logger.critical(f'It takes {(time.time() - start) / 60: .2f} minutes for execution')

if __name__ == "__main__":
    parser = get_args()
    args = parser.parse_args()
    main(args)

