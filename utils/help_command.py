from aiogram import types


async def help_command(message):
    text = ("Список команд: ",
            "/start - Начать диалог",
            "/help - Получить справку")

    await message.answer("\n".join(text))