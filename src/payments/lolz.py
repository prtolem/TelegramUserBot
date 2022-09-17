import asyncio
from datetime import datetime, timedelta
import re
import requests

from aiohttp import ClientSession
from bs4 import BeautifulSoup
from Crypto.Cipher import AES
from pyrogram import Client

from ..config import Config

config = Config.load_from_file("config.toml")


class LolzPayment:
    def __init__(self, amount, comment, cookies):
        self.amount = amount
        self.comment = comment
        self.cookies = cookies
        self.bill_created_at = datetime.now()

    async def check_bill(self, client: Client, userid: int):
        headers = {
            'authority': 'lolz.guru',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'ru,en;q=0.9',
            'cookie': self.cookies,
            'if-modified-since': 'Fri, 16 Sep 2022 18:02:09 GMT',
            'referer': 'https://lolz.guru/',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Yandex";v="22"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.167 YaBrowser/22.7.5.1027 Yowser/2.5 Safari/537.36',
        }
        async with ClientSession() as session:
            res = True
            while res and datetime.now() < self.bill_created_at + timedelta(minutes=int(config.payment_settings.time_check / 60)):
                async with session.get(f'https://lolz.guru/market/user/{config.lolz.userid}/payments',
                                       headers=headers) as response:
                    soup = BeautifulSoup(await response.text(), 'html.parser')
                    for i in soup.find_all('div', class_='muted comment')[0:3]:
                        if i.text.strip() == self.comment:
                            res = False
                            await client.send_message(userid, f'Ты оплатил счет на {self.amount} рублей, спасибо!😘')
                            return
                    await asyncio.sleep(10)


class LolzCookies:
    def __init__(self):
        self.df_id_pattern = re.compile(
            r'document\.cookie\s*=\s*"([^="]+)="\s*\+\s*toHex\(slowAES\.decrypt\(toNumbers\(\"([0-9a-f]{32})\"\)',
            re.MULTILINE)
        self.headers = {
            'authority': 'lolz.guru',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
            'x-ajax-referer': 'https://lolz.guru/',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'x-requested-with': 'XMLHttpRequest',
            'sec-ch-ua-platform': '"Windows"',
            'origin': 'https://lolz.guru',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://lolz.guru/',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'cookie': f'xf_user={config.lolz.xf_user}; xf_tfa_trust={config.lolz.xf_tfa_trust}; xf_logged_in=1;'
        }

    def get_df_uid(self, soup: BeautifulSoup):
        noscript = soup.find("noscript")
        if not noscript:
            return False
        pstring = noscript.find("p")
        if not (
                pstring
                and pstring.string
                == "Oops! Please enable JavaScript and Cookies in your browser."
        ):
            return False
        script = soup.find_all("script")
        if not script:
            return False
        if not (
                script[1].string.startswith(
                    'var _0xe1a2=["\\x70\\x75\\x73\\x68","\\x72\\x65\\x70\\x6C\\x61\\x63\\x65","\\x6C\\x65\\x6E\\x67\\x74\\x68","\\x63\\x6F\\x6E\\x73\\x74\\x72\\x75\\x63\\x74\\x6F\\x72","","\\x30","\\x74\\x6F\\x4C\\x6F\\x77\\x65\\x72\\x43\\x61\\x73\\x65"];function '
                )
                and script[0].get("src") == "/aes.js"
        ):
            return False
        match = self.df_id_pattern.search(script[1].string)

        cipher = AES.new(
            bytearray.fromhex("e9df592a0909bfa5fcff1ce7958e598b"),
            AES.MODE_CBC,
            bytearray.fromhex("5d10aa76f4aed1bdf3dbb302e8863d52"),
        )
        return [match.group(1), cipher.decrypt(bytearray.fromhex(match.group(2))).hex()]

    def get_cookies(self):
        response = requests.get("https://lolz.guru/", headers=self.headers)
        soup = BeautifulSoup(response.text, "html.parser")
        cookie = self.get_df_uid(soup)
        return self.headers['cookie'] + f' {cookie[0]}={cookie[1]};'
