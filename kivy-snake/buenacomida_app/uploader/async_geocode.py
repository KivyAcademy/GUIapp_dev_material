import asyncio
from aiohttp import ClientSession
from urllib.parse import urlencode
import json


_semaphore = 100

url = 'https://maps.googleapis.com/maps/api/geocode/json?{}' \
      '&key=AIzaSyDVVAh1A6H2wjgB6JEHpAhu3BDaD1_Jjr0'


async def fetch(address, session):
    async with session.get(url.format(urlencode({'address': address}))) as response:
        res = await response.read()
        results[address] = res
        return res


async def bound_fetch(sem, address, session):
    # Getter function with semaphore.
    async with sem:
        await fetch(address, session)


async def run(addresses):
    # create instance of Semaphore
    sem = asyncio.Semaphore(_semaphore)

    # Create client session that will ensure we dont open new connection
    # per each request.
    async with ClientSession() as session:
        tasks = [asyncio.ensure_future(bound_fetch(sem, address, session))
                 for address in addresses]

        responses = asyncio.gather(*tasks)
        await responses


results = {}
def geocode_adresses(addresses):

    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(run(addresses))
    loop.run_until_complete(future)


with open('30k.json') as jsonfile:
    restaurants = json.load(jsonfile)

