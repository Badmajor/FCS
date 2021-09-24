from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import line3_callback


def line3_keyboard(list_user: list):
    keyboard = InlineKeyboardMarkup(row_width=2)
    for data in list_user:
        s = ''
        if data.get('verification') == 1:
            s = '✅'
        keyboard.insert(InlineKeyboardButton(
            text=data.get("user_name")+s, callback_data=line3_callback.new(
                user_id=data.get('user_id'), phone=data.get('phone')+'  @'+data.get('user_name'),
                ver=data.get('verification')))
        )
    keyboard.row(InlineKeyboardButton(
        text='<- Назад', callback_data=line3_callback.new(user_id=0, phone=0, ver='menu')
    ))
    return keyboard


def line3_keyboard_ver(list_user: list, call):
    keyboard = InlineKeyboardMarkup(row_width=2)
    id = call.data.split(':')[1]
    buttons = []
    for data in list_user:
        s = ''
        if data.get('verification') == 1:
            s = '✅'
        buttons.append(InlineKeyboardButton(
            text=data.get("user_name")+s, callback_data=line3_callback.new(
                user_id=data.get('user_id'), phone=data.get('phone')+'  @'+data.get('user_name'),
                ver=data.get('verification')))
        )
    keyboard.row(InlineKeyboardButton(
        text='Верифицировать!', callback_data=line3_callback.new(
            user_id=id, phone=0, ver='go_pay')
    ))
    keyboard.add(*buttons)
    keyboard.add(InlineKeyboardButton(
        text='<- Назад', callback_data=line3_callback.new(user_id=0, phone=0, ver='menu')
    ))
    return keyboard
