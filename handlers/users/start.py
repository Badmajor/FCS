from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from handlers.users.menu import start_menu
from loader import dp, bot
import logging

from utils.db_api.check_status import check_status_user


@dp.message_handler(CommandStart(), chat_type='private')
async def bot_start(message: types.Message):
    if await check_status_user(message.from_user.id) != 'no_reg':
        await start_menu(message)
    else:
        logging.info(f'Зупустил {message.from_user.username},{message.from_user.first_name},'
                     f'{message.from_user.last_name}')
        await message.answer(f"Привет, {message.from_user.first_name}!\n\n "
                             "Для начала регистрации введи команду /reg\n\n"
                             f"У нас есть чат, если у тебя есть какие-то вопросы\n"
                             f"https://t.me/FCS_chat")
