from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import squad_keyboard_callback, menu_callback


def make_squad_keyboard(list_squad:list):
    keyboard = InlineKeyboardMarkup(row_width=2)
    for data in list_squad:
        keyboard.insert(InlineKeyboardButton(
            text=data.get('user_name'), callback_data=squad_keyboard_callback.new(
                user_id=data.get('user_id'), user_name=data.get('user_name'),ver=data.get('verification')))
        )
    keyboard.add(InlineKeyboardButton(
        text='<- Назад',callback_data=menu_callback.new(status='ver', command='main')
    ))
    return keyboard
