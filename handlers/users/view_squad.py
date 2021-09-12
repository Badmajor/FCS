from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import squad_keyboard_callback, menu_callback, line3_callback
from loader import dp
from utils.db_api.check_status import check_status_invite
from utils.db_api.get_data_db import get_user_data


@dp.callback_query_handler(squad_keyboard_callback.filter())
async def view_squad(call: CallbackQuery, callback_data: dict):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data=menu_callback.new(
        status='ver', command='squad')))
    user_data = await get_user_data(callback_data.get('user_id'), db=False)
    ver = 'Не пройдена'
    if user_data.get('verification'):
        ver = 'Пройдена'
    status_invite = [await check_status_invite(r) for r in  [user_data.get("ref_1"), user_data.get("ref_2")]]
    await call.answer(cache_time=5)
    await call.message.edit_text(
        f'{callback_data.get("user_name")}\n\n'
        f'Верификация: {ver}\n\n'
        f'Коды приглашения:\n'
        f'{user_data.get("ref_1")} - {status_invite[0]}\n'
        f'{user_data.get("ref_2")} - {status_invite[0]}'
        , reply_markup=keyboard
                                 )


@dp.callback_query_handler(line3_callback.filter())
async def line3_view(call: CallbackQuery, callback_data: dict):
    pass
