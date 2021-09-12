from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import menu_callback, line3_callback


def line3_keyboard(list_user:list):
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
        text='<- Назад', callback_data=menu_callback.new(status='ver', command='main')
    ))
    return keyboard