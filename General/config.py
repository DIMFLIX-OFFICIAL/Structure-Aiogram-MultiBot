from asyncio import AbstractEventLoop
from dataclasses import dataclass, field
from typing import Optional, Dict

from pyngrok import ngrok
from aiogram import Bot, Dispatcher
from environs import Env

from General.database import DB


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


@dataclass(slots=True)
class Meta(metaclass=Singleton):
    logging_for_bots: bool
    webhook_host: str
    webhook_port: int
    web_url: str
    webhook_path: str
    all_bots: Dict = field(default_factory=dict)


@dataclass
class BotData:
    id: int
    token: str
    admin_id: int
    is_meta_bot: bool
    db_name: str
    bot: Bot
    dp: Dispatcher
    db: DB
    loop: AbstractEventLoop


@dataclass(slots=True)
class MainBot:
    token: str
    admin_id: int
    db_name: str


@dataclass(slots=True)
class Payments:
    qiwi_token: str
    yoomoney_token: str


@dataclass(slots=True)
class Config:
    main_bot: MainBot
    payments: Payments
    meta: Meta


def cfg(path: Optional[str] = None) -> Config:
    env = Env()
    env.read_env(path)
    port = env.int("WEBHOOK_PORT", default=5000)

    return Config(
        main_bot=MainBot(
            token=env.str('BOT_TOKEN'),
            admin_id=env.int('ADMIN_ID'),
            db_name=env.str('DB_NAME')
        ),
        payments=Payments(
            qiwi_token=env.str('QIWI_TOKEN', default=None),
            yoomoney_token=env.str('YOOMONEY_TOKEN', default=None),
        ),
        meta=Meta(
            logging_for_bots=env.bool("LOGGING_FOR_BOTS", default=False),
            webhook_host=env.str("WEBHOOK_HOST", default='localhost'),
            webhook_port=port,
            web_url=ngrok.connect(port).public_url if env.bool("AUTO_URL") else env.str("WEB_URL"),
            webhook_path="/webhook/{bot_token}"
        )
    )
