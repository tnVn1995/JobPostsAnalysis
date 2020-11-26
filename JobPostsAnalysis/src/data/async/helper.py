from aiohttp import ClientSession
import asyncio
URL = 'http://www.indeed.com/jobs?'

loc = 'Houston, TX'

title = "data scientist"

params = {'q': loc, 't': title}


if __name__ == "__main__":
    async def main():
        session = ClientSession()
        async with session.get(URL, params=params) as resp:
            print(str(resp.url)) 
            print(type(await resp.read()))
            # print(await resp.read())
            return 
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

    loop.close()