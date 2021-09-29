from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp
from utils.help_command import help_command


@dp.message_handler(CommandHelp(), chat_type='private')
async def bot_help(message: types.Message):
    await help_command(message)


@dp.message_handler(text_contains='help', chat_type='private')
async def bot_help(message: types.Message):
    await help_command(message)
