## Sequential Scraping
import time, requests, argparse, json, itertools
from typing import List, Dict, Union, Optional, Iterable

import random
from bs4 import BeautifulSoup
import pandas as pd


from proxyManager import ProxyManager
from Crawler import Crawler
from config import CONFIG, Query, JobInfo, JobDesc
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
	"""No info scraped"""
	pass

class FailedAttempt(Exception):
	"""exceeded 5 attempts"""
	pass

# Main 
def main(args):
	# Initialize configuration
	logger = setup_logger(name=__file__, logfile=CONFIG.log_path / 'seq_indeed.log', level=loglv[args.LOGLVL], maxBytes=1e6, backupCount=3)
	logger.debug(type(logger))
	start = time.time()
	# Initiate Indeed crawler
	crawler = Crawler()
	no_jobs = 0
	start_page = 0  # one input argument
	end_page = args.PAGE  # one input argument
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
	\t- Number of Pages to crawl per query: {end_page}\n 
	\t- Queries parameters: {params}\n
	\t- Job titles: {titles}''')
	print('\t- Starting Crawling ...')
	params_list = itertools.product(locations, titles)
	proxy_scraper = ProxyManager()
	jobInfo = []
	jobDesc = []
	for queries in params_list:
		start_page = 0
		proxy_scraper.update_proxy_list()
		while start_page <= end_page:
			query = Query(*queries, start_page*no_jobs)
			# query.sleep()
			logger.info(f"queue with {query.__dict__}...")
			try:
				divs = crawler.getJobPost(queries=query.__dict__, proxy_scraper=proxy_scraper)
				# TODO: when divs is not None if len(divs) = 0, no_jobs should not be changed
				if divs is not None:
					no_jobs = len(divs)
				else:
					raise FailedAttempt
				if not no_jobs:
					raise NojobError
			except FailedAttempt:
				logger.info("Failed to scrape info, moving on ...")	
				start_page += 1
				continue
			except NojobError:
				logger.info("Something's wrong, moving on ...")
				start_page += 1
				continue
			for div in divs:
				
				try:
					temp_info = JobInfo(*crawler.getInfo(div), query.l)
					logger.info("Getting job description...")
					job_description = crawler.getJobDes(temp_info.summarylink)
					jobdesc = JobDesc(temp_info.summarylink, job_description)
					jobInfo.append(temp_info.__dict__)
					jobDesc.append(jobdesc.__dict__)
					logger.info("Done! Continue...")
				except Exception as e:
					logger.error(f"Encounter {e}")
			start_page += 1
			logger.info(f"Done scraping for position {query.q} at {query.l}, total number of jobs scraped {len(jobInfo)}")
	infoDf = pd.DataFrame(jobInfo)
	infoDf = infoDf.drop_duplicates()
	jobdescDf = pd.DataFrame(jobDesc)
	jobdescDf = jobdescDf.drop_duplicates()
	logger.critical(f'Saving raw data to {str(CONFIG.data_path / "raw")}...')
	jobdescDf.to_csv(str(CONFIG.data_path / 'raw' / 'jobdescRaw.csv'), index=False)
	infoDf.to_csv(str(CONFIG.data_path / 'raw') + '/jobpostsRaw.csv', index=False)
	time.sleep(1)
	logger.info("Done scraping from Indeed!")
	logger.critical(f'It takes {(time.time() - start) / 60: .2f} minutes for execution')
def crawl_page() -> None:
	pass
# # TODO: Parallelizing web scraping
# 	for l in locations:
# 	    proxy_scraper = ProxyManager()
# 	    for t in titles:
# 	        proxy_scraper.update_proxy_list()
# 	        for page in range(start_page, end_page):
# 	            randomSleep = random.randint(3,6)
# 	            logger.info(f"Sleep for {randomSleep}")
# 	            time.sleep(randomSleep)
# 	            logger.info(f"Start scraping ...")
# 	            proxy = proxy_scraper.get_proxy()
# 	            params['q'] = t
# 	            params['l'] = l
# 	            params['start'] = page * no_jobs
# 	            logger.info(' Getting information from the provided URL...')
# 	            logger.debug(f"queue with {params}...")
# 	            divs = crawler.getJobPost(queries=params, proxy=proxy)
# 	            # TODO: fix codes to account for when the job pages is less than end_page
# 	            # *Hint: the pagination class in ul shows the number of pages for a search query
# 	            if divs is not None:
# 	                no_jobs = len(divs)
# 	            elif divs is None:
# 	                logger.info("Something's wrong, moving on...")
# 	                continue
# 	            logger.info(f' The number of job postings found is {no_jobs}')
# 	            for div in divs:
# 	                temp_info = crawler.getInfo(div)
# 	                # TODO: Insert codes to retrieve job des and loc here
# 	                temp_info['location'] = params['l']
# 	                logger.info(f"Getting job description...")
# 	                jobdesc = crawler.getJobDes([temp_info['summarylink']])
# 	                JobDesc.append(jobdesc)
# 	                JobInfo.append(temp_info)
# 	            # TODO: Fix code to use database instead of csv file
# 	            # TODO: Ensure that if there are no jobs, crawler escape loop
# 	            logger.info(f" Done scraping for position {params['q']} at {params['l']}, job number from {params['start']}")
# 	            logger.info(f" Continue with next query")
# 	data = pd.DataFrame(JobInfo)
# 	data = data.drop_duplicates()
# 	logger.critical(f'Saving raw data to {str(CONFIG.data_path / "raw")}...')
# 	data.to_csv(str(CONFIG.data_path / 'raw') + '/jobpostsRaw.csv', index=False)
# 	time.sleep(1)
# 	logger.info("Done scraping from Indeed!")
# 	logger.critical(f'It takes {(time.time() - start) / 60: .2f} minutes for execution')

if __name__ == "__main__":
	parser = get_args()
	args = parser.parse_args()
	main(args)

