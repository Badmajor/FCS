from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp
from utils.help_command import help_command


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    await help_command(message)


@dp.callback_query_handler(text_contains='help')
async def bot_help(message: types.Message):
    await help_command(message)
