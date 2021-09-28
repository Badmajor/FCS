from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from loader import dp


# Эхо хендлер, куда летят текстовые сообщения без указанного состояния


'''@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    await message.answer(f"Используйте только "
                         f"доступные команды\n"
                         f"/Start\n"
                         f"/Help\n"
                         f"/Reg\n"
                         f"/Menu\n
                         f"/Docs"")'''


@dp.message_handler(Text(equals="отмена", ignore_case=True), state='*')
async def all_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(f'Отменил!')
    await message.answer(f"Доступные команды\n"
                         f"/Start\n"
                         f"/Help\n"
                         f"/Reg\n"
                         f"/Menu\n"
                         f"/Docs")


# Эхо хендлер, куда летят ВСЕ сообщения с указанным состоянием
'''@dp.message_handler(state="*", content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    state = await state.get_state()
    await message.answer(f"Эхо в состоянии <code>{state}</code>.\n"
                         f"\nСодержание сообщения:\n"
                         f"<code>{message}</code>")'''
