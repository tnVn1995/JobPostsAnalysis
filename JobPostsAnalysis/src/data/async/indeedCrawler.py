import asyncio
from socket import timeout
from typing import List, Tuple, Dict


from aiohttp import ClientSession
import aiohttp
from aiohttp.client import request
from aiohttp.client_exceptions import ClientError
from urllib.parse import urljoin, urlparse

from logzero import setup_logger


from config import CONFIG


logger = setup_logger(name=__file__, logfile=CONFIG.log_path / 'indeedCrawler.log')

class AsyncCrawler:
    def __init__(self, start_url:str='http://www.indeed.com/jobs?', max_concurrency=200):
        self.start_url = start_url
        self.base_url = f"{urlparse(self.start_url).scheme}://{urlparse(self.start_url).netloc}"
        self.bounded_semaphore = asyncio.BoundedSemaphore(max_concurrency)

    async def _http_request(self, url: str, params: Dict[str, str]) -> str:

        self._session = ClientSession()
        logger.info(f"Fetching: {url}")
        async with self.bounded_sempahore:
            try:
                async with self._session.get(url, timeout=30) as response:
                    html = await response.read()
                    return html
            except Exception as e:
                logger.warning(f'Exception: {e}')
    @staticmethod
    def debug_helper(url: str='http://www.indeed.com/jobs?') -> str:

        async def main():
            loc = 'Houston, TX'

            title = "data scientist"

            params = {'q': loc, 't': title}
            session = ClientSession()
            async with session.get(url, params=params) as resp:
                print(str(resp.url)) 
                print(type(await resp.read()))
                # print(await resp.read())
                return await resp.read()
            
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
        loop.close()
if __name__ == "__main__":
    pass
                

