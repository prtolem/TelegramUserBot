import asyncio
from datetime import datetime, timedelta

from glQiwiApi import QiwiP2PClient
from pyrogram import Client

from ..config import Config

config = Config.load_from_file("config.toml")


class QiwiPayment:
    def __init__(self, amount: int):
        self.amount = amount
        self.bill_id = None

    async def create_bill(self):
        async with QiwiP2PClient(secret_p2p=config.qiwi.p2p_token) as p2p:
            bill = await p2p.create_p2p_bill(amount=self.amount, expire_at=datetime.now() + timedelta(minutes=int(config.payment_settings.time_check / 60)))
        self.bill_id = bill.id
        return bill.pay_url

    async def check_bill(self, client: Client, userid: int):
        async with QiwiP2PClient(secret_p2p=config.qiwi.p2p_token) as p2p:
            bill_status = await p2p.get_bill_status(bill_id=self.bill_id)
            while bill_status != 'PAID' and bill_status != 'EXPIRED':
                await asyncio.sleep(10)
                bill_status = await p2p.get_bill_status(bill_id=self.bill_id)
            if await p2p.get_bill_status(self.bill_id) == 'PAID':
                await client.send_message(userid, f'Ты оплатил счет на {self.amount} рублей, спасибо!😘')
