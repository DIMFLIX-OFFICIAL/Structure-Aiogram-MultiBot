import inspect
from functools import partial as fcpartial

from BotCore.handlers.users import start
from General.config import BotData


class UsersRoutes:
    """
    This class is created for registering handlers.
    In it, you can separate registrations from different files into functions to make it easier to use.
    Also, when registering, we can wrap the handler in the "fcpartial" function, which
     allows us to pass additional parameters.
     As mandatory additional parameters, we pass the "BotData" data class, which contains all the necessary
      class instances, namely dispatcher, bot, db, etc.
    """

    __slots__ = ("bot_data", "create_bot")

    def __init__(self, bot_data: BotData, create_bot):
        self.bot_data = bot_data  # BotData
        self.create_bot = create_bot  # CreateBot class

        ##==> AUTO START ALL FUNCTIONS
        ########################################
        for i in inspect.getmembers(self, predicate=inspect.ismethod):
            if i[0] != "__init__":
                i[1]()

    def register_start_handlers(self):
        self.bot_data.dp.register_message_handler(
            fcpartial(start.bot_start_command, bot_data=self.bot_data),
            commands=["start"],
            state="*"
        )
