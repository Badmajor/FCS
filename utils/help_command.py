

async def help_command(message):
    text = ("Список документов: ",
            "/start - Начать диалог",
            "/help - Получить справку",
            "/reg - Зарегистрироваться",
            "/menu - Войти в меню личного кабинета",
            "/docs - Ознакомиться с документами проекта")
    await message.answer("\n".join(text))
