from aiohttp import ClientSession


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