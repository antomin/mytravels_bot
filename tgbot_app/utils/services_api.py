from aiohttp import ClientSession


class Aviasales:
    def __init__(self, token):
        self.token = token
        self.headers = {'Accept-Encoding': 'gzip, deflate'}

    async def search_flights(self, depart_code, arrival_code, date_depart, date_return, is_direct, one_result=None):
        url = 'https://api.travelpayouts.com/aviasales/v3/prices_for_dates'

        params = {
            'origin': depart_code,
            'destination': arrival_code,
            'departure_at': date_depart,
            'direct': is_direct,
            'token': self.token,
            'one_way': 'true' if one_result else 'false'
        }

        if date_return:
            params['return_at'] = date_return

        async with ClientSession() as session:
            async with session.get(url=url, params=params, headers=self.headers) as response:
                result = await response.json(content_type=response.content_type)

        return result['data']


class Sputnik:
    def __init__(self, token, username):
        self.token = token
        self.username = username
        self.params = {
            'api_key': self.token,
            'username': self.username,
            'limit': 50
        }

    async def get_categories(self, city_id):
        url = f'https://api.sputnik8.com/v1/cities/{city_id}/categories'

        async with ClientSession() as session:
            async with session.get(url=url, params=self.params) as response:
                data = await response.json(content_type=response.content_type)

        result = {}

        for cat in data[0]['sub_categories']:
            cnt_products = len(cat['products'])
            if cnt_products:
                result[str(cat['id'])] = {
                    'title': cat['short_name'],
                    'products': cat['products'],
                    'cnt': cnt_products
                }

        return result

    async def get_product_detail(self, product_id):
        url = f'https://api.sputnik8.com/v1/products/{product_id}'

        async with ClientSession() as session:
            async with session.get(url=url, params=self.params) as response:
                data = await response.json(content_type=response.content_type)

        return data


class Exchangerate:
    @staticmethod
    async def get_latest(base, other):
        url = 'https://api.exchangerate.host/latest'

        params = {
            'base': base,
            'symbols': other
        }

        async with ClientSession() as session:
            async with session.get(url=url, params=params) as response:
                data = await response.json(content_type=response.content_type)

        if response.ok and data['success'] and len(data["rates"]) == 1:
            return f'1 {data["base"]} = {round(data["rates"][other], 2)} {other}'
        else:
            return

    @staticmethod
    async def get_convert(amount, _from, _to):
        url = 'https://api.exchangerate.host/convert'

        params = {
            'from': _from,
            'to': _to,
            'amount': amount
        }

        async with ClientSession() as session:
            async with session.get(url=url, params=params) as response:
                data = await response.json(content_type=response.content_type)

        if response.ok and data['success'] and data['result']:
            return f'{amount} {_from} = {round(data["result"], 2)} {_to}'
        else:
            return

    @staticmethod
    async def get_symbols():
        url = 'https://api.exchangerate.host/symbols'

        async with ClientSession() as session:
            async with session.get(url=url) as response:
                data = await response.json(content_type=response.content_type)

        if response.ok and data['success']:
            return '\n'.join([f'{el["code"]} - {el["description"]}' for el in data['symbols'].values()])
        else:
            return
