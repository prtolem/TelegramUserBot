import asyncio

from aiohttp import ClientSession
from datetime import datetime, timedelta

from ..config import Config

config = Config.load_from_file("config.toml")


class CryptoPay:
    def __init__(self, amount, order_id):
        self.amount = amount
        self.order_id = order_id
        self.uuid = None
        self.invoice_created_at = None
        self.headers = {'Authorization': f'Token {config.cryptocloud.token}',}

    async def create_bill(self):
        async with ClientSession() as session:
            payload = {
                'shop_id': config.cryptocloud.shop_id,
                'amount': self.amount,
                'order_id': self.order_id,
                'currency': 'RUB',
            }
            async with session.post('https://cryptocloud.plus/api/v2/invoice/create', headers=self.headers, json=payload) as response:
                response = await response.json()
                self.uuid = response['invoice_id']
                self.invoice_created_at = datetime.now()
                return response['pay_url']

    async def check_bill(self, client, userid):
        await asyncio.sleep(5)
        async with ClientSession() as session:
            while self.invoice_created_at + timedelta(minutes=int(config.payment_settings.time_check / 60)) > datetime.now():
                async with session.get(f'https://cryptocloud.plus/api/v2/invoice/status?uuid={self.uuid}', headers=self.headers) as response:
                    if response.status == 200 and (await response.json())['status_invoice'] == 'paid':
                        await client.send_message(userid, f'Ты оплатил счет на {self.amount} рублей, спасибо!😘')
                        break
                    await asyncio.sleep(10)
