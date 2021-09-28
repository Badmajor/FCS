from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp


@dp.message_handler(text_contains='docs', state='*')
async def docs_pr(message: types.Message, state: FSMContext):
    await state.finish()
    text = ("Список документов: ",
            "Пользовательское Соглашение:",
            "https://telegra.ph/Polzovatelskoe-soglashenie-09-23-3",
            "",
            "FAQ:",
            "https://telegra.ph/Pomoshch-nuzhna-09-08",
            "")
    await message.answer("\n".join(text))