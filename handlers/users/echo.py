from aiogram import types
from loader import dp


# Эхо хендлер, куда летят текстовые сообщения без указанного состояния


@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    await message.answer(f"Используйте только "
                         f"доступные команды\n"
                         f"/Start\n"
                         f"/Help\n"
                         f"/Reg\n"
                         f"/Menu\n")


# Эхо хендлер, куда летят ВСЕ сообщения с указанным состоянием
'''@dp.message_handler(state="*", content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    state = await state.get_state()
    await message.answer(f"Эхо в состоянии <code>{state}</code>.\n"
                         f"\nСодержание сообщения:\n"
                         f"<code>{message}</code>")'''
