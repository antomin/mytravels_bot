from aiohttp import ClientSession


class Aviasales:
    def __init__(self, token):
        self.token = token
        self.headers = {'Accept-Encoding': 'gzip, deflate'}

    async def search_flights(self, depart_code, arrival_code, date_depart, date_return, is_direct):
        url = 'https://api.travelpayouts.com/aviasales/v3/prices_for_dates'

        params = {
            'origin': depart_code,
            'destination': arrival_code,
            'departure_at': date_depart,
            'direct': is_direct,
            'token': self.token
        }

        if date_return:
            params['return_at'] = date_return
            params['one_way'] = 'false'

        async with ClientSession() as session:
            async with session.get(url=url, params=params, headers=self.headers) as response:
                result = await response.json()

        return result['data']
