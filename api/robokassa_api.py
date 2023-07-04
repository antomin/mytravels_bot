import hashlib
from aiohttp import ClientSession
from urllib.parse import urlencode

from django.conf import settings


class Robokassa:
    def __init__(self, login, pass_1, pass_2):
        self.login = login
        self.pass_1 = pass_1
        self.pass_2 = pass_2

    def gen_payment_link(self, user_id, order_id, amount=None, desc=None, prev_payment=None):
        url = f'https://auth.robokassa.ru/Merchant/{"Index.aspx" if not prev_payment else "Recurring"}'

        if desc is None:
            desc = f'Поддержка автора MyTravels | {user_id}'
        if amount is None:
            amount = settings.SUBSCRIPTION_PRICE
        signature = self.__create_signature(self.login, amount, order_id, self.pass_1)

        data = {
            'MerchantLogin': self.login,
            'OutSum': amount,
            'invoiceID': order_id,
            'Description': desc,
            'SignatureValue': signature,
        }
        if prev_payment:
            data['PreviousInvoiceID'] = prev_payment
            data['Recurring'] = True

        return f'{url}?{urlencode(data)}'

    async def send_recurring_payment(self, user_id, order_id, prev_order_id):
        url = 'https://auth.robokassa.ru/Merchant/Recurring'
        desc = f'Продление поддержки автора MyTravels | {user_id}'
        signature = self.__create_signature(self.login, settings.SUBSCRIPTION_PRICE, order_id, self.pass_1)

        payload = {
            'MerchantLogin': self.login,
            'OutSum': settings.SUBSCRIPTION_PRICE,
            'InvoiceId': order_id,
            'PreviousInvoiceID': prev_order_id,
            'Description': desc,
            'SignatureValue': signature,
        }

        async with ClientSession() as session:
            async with session.post(url=url, data=payload) as response:
                print(await response.text())

    def check_signature_response(self, order_id, amount, received_signature):
        signature = self.__create_signature(amount, order_id, self.pass_1)
        return signature == received_signature

    @staticmethod
    def __create_signature(*args):
        return hashlib.md5(':'.join(str(el) for el in args).encode()).hexdigest()
