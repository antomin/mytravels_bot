import asyncio

from aiohttp import ClientSession


class Aviasales:
    def __init__(self, token, marker):
        self.token = token
        self.marker = marker
        self.headers = {'Accept-Encoding': 'gzip, deflate'}
        self.semaphore = asyncio.Semaphore(10)

    async def search_flights(self, depart_code, arrival_code, date_depart, date_return, is_direct, one_result=None):
        url = 'https://api.travelpayouts.com/aviasales/v3/prices_for_dates'

        params = {
            'origin': depart_code,
            'destination': arrival_code,
            'departure_at': date_depart,
            'direct': is_direct,
            'token': self.token,
            'one_way': 'false'
        }

        if date_return:
            params['return_at'] = date_return

        async with self.semaphore:
            async with ClientSession() as session:
                async with session.get(url=url, params=params, headers=self.headers) as response:
                    result = await response.json(content_type=response.content_type)

        if one_result:
            return [result['data'][0]]

        return result['data']

    async def gen_link(self, link):
        return f'https://aviasales.com{link}&marker={self.marker}'
