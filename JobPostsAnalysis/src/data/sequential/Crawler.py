from bs4 import BeautifulSoup
import pandas as pd
import time, requests, argparse, json
from typing import List, Dict, Union, Optional


from config import CONFIG
from proxyManager import ProxyManager
from logzero import setup_logger

CrawlerLogger = setup_logger(name=__file__, logfile=CONFIG.log_path / 'seq_err.log', maxBytes=10000, backupCount=5)

class Crawler():
    """Job Posts crawler from Indeed"""
    def __init__(self) -> None:
        pass
    def getInfo(self, div:BeautifulSoup) -> Dict:
        """Take input as a bs4 tag and return a dict with information about
        a job posting

        Args:
            div (BeautifulSoup): a bs4 tag of job postin

        Returns:
            Dict: return a dictionary with information about job title, summary link to job description,
            job location, company name
        """       
        for a in div.find_all('a', attrs={'data-tn-element': 'jobTitle'}):
            title = a.text
            summarylink = a['href']
        for Name in div.find_all('span', attrs={'class': 'company'}):
            name = Name.text

        return title, summarylink, name


    def getJobPost(self, proxy_scraper: ProxyManager, URL:str='http://www.indeed.com/jobs?', queries:Optional[dict]=None) -> BeautifulSoup:
        """[Get list of job postings from indeed]

        Keyword Arguments:
            proxy {str}: a live proxy
            URL {str} -- [Can be modified to scrape from other sites]
            (default: {'http://www.indeed.com/jobs?'})
            queries {dict} -- [queries to scrape] (default: {None})

        Returns:
            BeautifulSoup -- [description]
        """
        divs = None
        count = 0
        proxy = proxy_scraper.get_proxy()
        while count <= 5:
            try:
                page = requests.get(URL, params=queries, timeout=10, proxies={'http':proxy})
            except Exception as e:
                CrawlerLogger.error(e)
                CrawlerLogger.info("Try with a different proxy")
            else:
                if page is None:
                    CrawlerLogger.error('Not found page')
                else:
                    soup = BeautifulSoup(page.text, 'html.parser')
                    divs = soup.find_all(name='div', class_='jobsearch-SerpJobCard')
                    return divs
            count += 1
            proxy = proxy_scraper.get_proxy()
        CrawlerLogger.error(f"Stop scraping url {URL} after 5 failed attempts")
        return 

    def getJobDes(self, summary_link:str, base_web:str='https://www.indeed.com') -> Union[List[str], None]:
        """[Get job descriptions from Indeed]

        Args:
            summary_links (List[str]): [list of connecting links]
            base_web (str, optional): [base linke]. Defaults to 'https://www.indeed.com'.

        Returns:
            List[str]: [Return a list-like of jobdescriptions for each link provided]
        """        
        # TODO: retrieve location of the company in addition
        try:
            link = base_web + summary_link
            page = requests.get(link, timeout=10)
            soup = BeautifulSoup(page.text, 'html.parser')
            div = soup.find_all('div', attrs={'id': 'jobDescriptionText'})
            return link, div[0].text 
        except IndexError:
            CrawlerLogger.error('Here\'s what div looks like\n:', div)
            CrawlerLogger.error('URL:', link)
            return None
        


if __name__ == "__main__":
    pass