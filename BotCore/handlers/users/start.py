from aiogram import types
from aiogram.utils.markdown import hlink

from BotCore.keyboards.inline import inline_markups as inav
from General.config import BotData


async def bot_start_command(message: types.Message, bot_data: BotData):
    username_link = hlink(message.from_user.first_name, message.from_user.url)

    await bot_data.bot.send_message(
        chat_id=message.chat.id,
        text=f'Что тебя интересует, {username_link} ? 😏'
    )
    await bot_data.bot.delete_message(message.from_user.id, message.message_id)
