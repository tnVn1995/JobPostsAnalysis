import asyncio
import logging 
import aiohttp
from urllib.parse import urljoin, urlparse
from lxml import html as lh

class AsyncCrawler:
    def __init__(self, start_url, crawl_depth, max_concurrency=200):
        self.start_url = start_url
        self.base_url = f"{urlparse(self.start_url).scheme}://{urlparse(self.start_url).netloc}"
        self.crawl_depth = crawl_depth
        self.seen_urls = set()
        self.session = aiohttp.ClientSession()
        self.bounde_sempahore = asyncio.BoundedSemaphore(max_concurrency)

    async def _http_request(self, url):
            print(f'Fetching: {url}')
            async with self.bounde_sempahore:
                try:
                    async with self.session.get(url, timeout=30) as response:
                        html = await response.read()
                        return html
                except Exception as e:
                    logging.warning(f'Exception: {e}')
    
    def find_urls(self, html):
        found_urls = []
        dom = lh.fromstring(html)
        for href in dom.xpath('//a/@href'):
            url = urljoin(self.base_url, href)
            if url not in self.seen_urls and url.startswith(self.base_url):
                found_urls.append(url)
        return found_urls

    async def extract_async(self, url):
        data = await self._http_request(url)
        found_urls = set()
        if data:
            for url in self.find_urls(data):
                found_urls.add(url)
        return url, data, sorted(found_urls)

url = 'https://www.theguardian.com'
crawler = AsyncCrawler(start_url=url, crawl_depth=3)
loop = asyncio.get_event_loop()
def main():
    html = crawler._http_request(url)
    print(html) 

loop.run_until_complete(main())