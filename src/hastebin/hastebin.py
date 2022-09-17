from aiohttp import ClientSession


class HastebinPaste:
    def __init__(self, code):
        self.code = code
        self.session = None

    async def paste(self):
        data = {'content': self.code}
        async with self.session.post('https://hastebin.app/paste', json=data) as response:
            return f'https://hastebin.app/{await response.text()}'

    async def __aenter__(self):
        self.session = ClientSession()
        await self.session.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            return await self.session.__aexit__(exc_type, exc_val, exc_tb)
