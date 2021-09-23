from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import squad_keyboard_callback, back_menu


def make_squad_keyboard(list_squad: list):
    keyboard = InlineKeyboardMarkup(row_width=2)
    for data in list_squad:
        s = ''
        user_name = data.get('phone') if data.get("user_name") is None else data.get("user_name")
        phone = data.get('phone') if data.get("user_name") is None else data.get('phone') + '  @' + data.get(
            'user_name')
        if data.get('verification') == 1:
            s = '✅'
        keyboard.insert(InlineKeyboardButton(
            text=user_name+s, callback_data=squad_keyboard_callback.new(
                user_id=data.get('user_id'), phone=phone, ver=data.get('verification'))))
    keyboard.add(InlineKeyboardButton(
        text='<- Назад', callback_data=squad_keyboard_callback.new(user_id=0, phone='ver', ver='menu')
    ))
    return keyboard
