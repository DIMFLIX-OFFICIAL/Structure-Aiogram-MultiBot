from asyncio import get_event_loop
from traceback import format_exc
from typing import Union

from aiogram import Bot, Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from AiogramStorages.storages import SQLiteStorage

from BotCore.filters.callback_filters import CData, CDataStart, CDataEnd
from BotCore.handlers.users.routes import UsersRoutes
from BotCore.utils.set_bot_commands import set_default_commands
from General.database import DB
from General.config import cfg, BotData


class CreateBot:
    """
    This class is used to automatically create a bot.
    This is where the database, instances of bot classes, dispatcher, and others are created.
    To create a bot, you need to pass the required parameters and call the run method.
    If the bot starts successfully, then the date class Botdata will be added to the all_bots variable
    of the Meta class in the config. Funext in the entire program, you can access the bot token key and receive
    a Botdata instance containing all the instances necessary for the bot to work.
    """

    __slots__ = (
        'bot_id', 'token', 'admin_id', 'is_main_bot', 'db_name', 'loop', 'db'
    )

    def __init__(self, bot_id: int, token: str, admin_id: int, is_main_bot: bool, db_name: str):
        self.bot_id = bot_id
        self.token = token
        self.admin_id = admin_id
        self.is_main_bot = is_main_bot
        self.db_name = db_name

        self.loop = get_event_loop()
        self.db = DB(db_name=self.db_name, loop=self.loop)

    async def create_bot(self) -> Union[bool, BotData]:
        try:
            storage = SQLiteStorage(db_path="General/databases/" + self.db_name + ".db")
            bot = Bot(token=self.token, loop=self.loop)
            dp = Dispatcher(bot=bot, storage=storage, loop=self.loop)
            return BotData(
                id=self.bot_id, token=self.token, admin_id=self.admin_id,
                is_meta_bot=self.is_main_bot, db_name=self.db_name, bot=bot,
                dp=dp, db=self.db, loop=self.loop
            )
        except:
            print(format_exc())
            return False

    async def run(self):
        bot_data = await self.create_bot()
        if isinstance(bot_data, BotData):
            self.setup_filters(bot_data.dp)
            self.setup_middlewares(bot_data.dp)
            self.setup_handlers(bot_data)
            await self.db.create_tables()
            await set_default_commands(bot_data.dp)
            await bot_data.bot.set_webhook(
                url=cfg().meta.web_url + cfg().meta.webhook_path.format(bot_token=self.token)
            )
            cfg().meta.all_bots.update({self.token: bot_data})

    @staticmethod
    def setup_handlers(bot_data):
        UsersRoutes(bot_data, CreateBot)

    @staticmethod
    def setup_filters(dp):
        dp.filters_factory.bind(CData)
        dp.filters_factory.bind(CDataStart)
        dp.filters_factory.bind(CDataEnd)

    @staticmethod
    def setup_middlewares(dp):
        if cfg().meta.logging_for_bots:
            dp.setup_middleware(LoggingMiddleware())
