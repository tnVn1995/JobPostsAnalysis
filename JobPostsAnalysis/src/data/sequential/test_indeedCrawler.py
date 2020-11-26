from src.data.sequential.Crawler import Crawler
from src.data.sequential.proxyManager import ProxyManager
from src.data.sequential.config import CONFIG
from logzero import setup_logger
import pytest
import sys
import pandas as pd


logger = setup_logger(name=__file__)


@pytest.fixture(scope='module')
def single_setup():
    proxy_scraper = ProxyManager()
    indeedCrawler = Crawler()
    queries = {'q':'data scientist', 'l': 'Houston, TX'}
    data = {'crawler': indeedCrawler, 'queries': queries, 'proxy_scraper': proxy_scraper}
    return data

@pytest.fixture(scope='module')
def multi_setup():    
    proxy_scraper = ProxyManager()
    indeedCrawler = Crawler()
    locations = ['Houston, TX', 'Dallas, TX']
    titles = ['data scientist']
    no_jobs = 0
    start_page = 0
    end_page = 2
    return indeedCrawler, locations, titles, no_jobs, start_page, end_page, proxy_scraper


class Test_single:

    def test_getJobPost(self, single_setup):
        queries, indeedCrawler, proxy_scraper = single_setup['queries'], single_setup['crawler'], single_setup['proxy_scraper']
        proxy_scraper.update_proxy_list()
        proxy = proxy_scraper.get_proxy()
        divs = indeedCrawler.getJobPost(queries=queries, proxy = proxy)
        assert len(divs) > 0 # validate getJobPost results
        assert type(divs[0].text) == str #  
        temp_info = indeedCrawler.getInfo(divs[0])
        assert type(temp_info['title']) == str # Validate getInfo result
        assert len(temp_info) == 3
        link = temp_info['summarylink']
        jobDesc = indeedCrawler.getJobDes([link])
        assert isinstance(jobDesc, pd.DataFrame) # Validate get_jobdes result
        assert type(jobDesc['description'].values[0]) == str
        assert len(jobDesc['description'].values[0]) > 0


class Test_multi:
    def test_getJobPost(self, multi_setup):
        indeedCrawler, locations, titles, no_jobs, start_page, end_page, proxy_scraper = multi_setup
        params = {'explbl':'entry_level', 'jt':'fulltime'}
        jobInfo = []
        proxy_scraper.update_proxy_list()
        for loc in locations:
            for title in titles:
                proxy = proxy_scraper.get_proxy()
                for page in range(start_page + 1, end_page):
                    params['q'] = title
                    params['l'] = loc
                    params['start'] = page * no_jobs
                    divs = indeedCrawler.getJobPost(queries=params, proxy=proxy)
                    no_jobs = len(divs)
                    for div in divs:
                        temp_info = indeedCrawler.getInfo(div)
                        temp_info['location'] = params['l']
                        jobInfo.append(temp_info)
        assert len(jobInfo) > 0
        assert isinstance(jobInfo[0], dict)
        assert 'location' in jobInfo[0].keys() 
