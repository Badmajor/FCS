from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запустить бота"),
            types.BotCommand("reg", "Зарегистрироваться"),
            types.BotCommand("menu", "Войти в меню личного кабинета"),
            types.BotCommand("docs", "Ознакомиться с документами проекта")
        ]
    )
