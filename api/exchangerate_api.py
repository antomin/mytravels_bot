from aiohttp import ClientSession


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