from pydantic import BaseModel
import toml


class UserBot(BaseModel):
    api_id: int
    api_hash: str
    admin_id: int


class Payments(BaseModel):
    time_check: int


class Lolz(BaseModel):
    xf_user: str
    xf_tfa_trust: str
    username: str
    userid: str


class CryptoCloud(BaseModel):
    token: str
    shop_id: str


class Qiwi(BaseModel):
    p2p_token: str


class Config(BaseModel):
    userbot: UserBot
    qiwi: Qiwi
    lolz: Lolz
    cryptocloud: CryptoCloud
    payment_settings: Payments

    @classmethod
    def load_from_file(cls, filename: str):
        raw_config = toml.load(filename)
        return cls(**raw_config)
