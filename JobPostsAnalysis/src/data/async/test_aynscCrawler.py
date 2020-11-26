from aiohttp import ClientSession
import asyncio
import sys
sys.path.append('./')
import pytest
from indeedCrawler import AsyncCrawler

@pytest.mark.skip(reason='')
class TestClass:

    def test_debug_helper(self): 

        IndeedCrawler = AsyncCrawler()
        assert isinstance(type(IndeedCrawler.debug_helper()), str)

