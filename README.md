# Юзер Бот для Telegram

Данный бот создан для месенджера Telegram. Он позволяет управлять платежами, отправлять код на hastebin.app и много чего
другого
____
# Установка

1. Если у вас еще не установлен Python, то скачайте его с [официального сайта](https://www.python.org/downloads/) и
   установите необходимые библиотеки.
____
```cmd
    pip install -r requirements.txt
```
____
2. Отлично, теперь откройте файл `config.example.toml` и введите свои данные.
   Обязательны к заполнению являются все поля! Если вы не знаете как какие-либо значения, обратитесь к разделу "
   Заполнение конфига"
3. Переименуйте файл `config.example.toml` в `config.toml`
4. Запустите бота командой `python main.py`
____
# Заполнение конфига
____
## userbot
```toml
api_id = 1234567 # Ваш api_id
api_hash = "1234567890abcdef1234567890abcdef" # Ваш api_hash
admin_id = 123456789 # Ваш id в Telegram
```
Получить api_id и api_hash можно [здесь](https://my.telegram.org/apps)

Получить admin_id в Telegram можно [здесь](https://t.me/userinfobot)
____
## qiwi
```toml
token = "1234567890abcdef1234567890abcdef" # Ваш токен Qiwi
```
Получить токен Qiwi можно [здесь](https://p2p.qiwi.com/api)
____
## lolz
```toml
xf_user = "1234567890abcdef1234567890abcdef" # Кук xf_user на сайте lolz.guru
xf_tfa_trust = "1234567890abcdef1234567890abcdef" # Кук xf_session на сайте lolz.guru. Кук будет доступен если у вас включена 2фа
username = "username" # Ваш логин на сайте lolz.guru
userid = "131234" # Айди вашего аккаунта на сайте lolz.guru
```
Получить куки можно через расширение, которое можно скачать [здесь](https://www.editthiscookie.com/)

Получить userid можно [здесь](https://lolz.guru/account/personal-details)

![Alt-текст](https://imgur.com/jICrTcF.png)
____
## cryptocloud
```toml
token = "1234567890abcdef1234567890abcdef" # Ваш токен Cryptocloud
shop_id = 123456789 # Ваш shop_id в Cryptocloud
```
Для получения токена и shop_id вам нужно зарегистрироваться [здесь](https://cryptocloud.plus/app/registration)
и создать новый проект [здесь](https://cryptocloud.plus/app/integration).
После, в правой части экрана будет написаны ваши токен и shop_id
![Alt-текст](https://imgur.com/xCKGuVS.png)
____
## payment
```toml
time_check = 1800 # Сколько секунд бот будет проверять платеж
```
Укажите время в секундах сколько бот будет проверять счета на оплату
____
# Команды
```
!киви сумма - Создать счет на оплату Qiwi
!лолз сумма комментарий - Создать счет на оплату Lolz
!крипто сумма идентификатор - Создать счет на оплату Cryptocloud
!код - Загрузить текст сообщения на которое ответили командой на hastebin.app
```