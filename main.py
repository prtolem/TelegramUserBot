from loguru import logger
from pyrogram import Client, filters
from pyrogram.types import Message

from src.config import Config
from src.payments.lolz import LolzCookies, LolzPayment
from src.payments.qiwi import QiwiPayment
from src.payments.crypto import CryptoPay
from src.hastebin.hastebin import HastebinPaste

lolz_cookies = LolzCookies().get_cookies()
config = Config.load_from_file("config.toml")

app = Client('my_account', api_id=config.userbot.api_id, api_hash=config.userbot.api_hash)


@app.on_message(filters=filters.command(prefixes='!', commands='киви'))
async def qiwi_payment(client: Client, message: Message):
    if message.from_user.id == config.userbot.admin_id:
        qiwi = QiwiPayment(amount=int(message.text.split()[1]))
        bill = await qiwi.create_bill()
        app.loop.create_task(qiwi.check_bill(client, message.chat.id))
        await message.edit_text(
            f'💰Оплати счет ({message.text.split()[1]} рублей) по <a href={bill}>ссылке</a>\n\n(Счет действителен {int(config.payment_settings.time_check / 60)} минут)')


@app.on_message(filters=filters.command(prefixes='!', commands='лолз'))
async def lolz_payment(client: Client, message: Message):
    if message.from_user.id == config.userbot.admin_id:
        lolz = LolzPayment(amount=int(message.text.split()[1]), comment=str(message.text.split()[2]),
                           cookies=lolz_cookies)
        app.loop.create_task(lolz.check_bill(client, message.chat.id))
        await message.edit_text(
            f'💰Оплати счет ({message.text.split()[1]} рублей) по <a href=https://lolz.guru/market/balance/transfer?amount={message.text.split()[1]}&username={config.lolz.username}&comment={message.text.split()[2]}>ссылке</a>\n\n(Счет действителен {int(config.payment_settings.time_check / 60)} минут)')


@app.on_message(filters=filters.command(prefixes='!', commands='крипта'))
async def crypto_payment(client: Client, message: Message):
    if message.from_user.id == config.userbot.admin_id:
        crypto = CryptoPay(amount=int(message.text.split()[1]), order_id=str(message.text.split()[2]))
        await message.edit_text(f'💰Оплати счет ({message.text.split()[1]} рублей) по <a href={await crypto.create_bill()}>ссылке</a>\n\n(Счет действителен {int(config.payment_settings.time_check / 60)} минут)')
        app.loop.create_task(crypto.check_bill(client, message.chat.id))


@app.on_message(filters=filters.command(prefixes='!', commands='код'))
async def code_paste(client: Client, message: Message):
    if message.from_user.id == config.userbot.admin_id:
        if message.reply_to_message:
            async with HastebinPaste(message.reply_to_message.text) as paste:
                try:
                    await message.reply_to_message.delete()
                except:
                    pass
                await message.edit_text(f'📝Код: <a href={await paste.paste()}>ссылка</a>')


if __name__ == '__main__':
    logger.success('Бот успешно начал свою работу! Подожди еще несколько секунд прежде чем начать работу!')
    app.run()
