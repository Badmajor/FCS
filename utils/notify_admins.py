

from aiogram import Dispatcher



async def on_startup_notify(dp: Dispatcher):
    await dp.bot.send_message(530291098, "Бот Запущен")


async def completed_squad(dp: Dispatcher):
    await dp.bot.send_message(530291098, "Squad закрыт")

