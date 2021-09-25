from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import invite_callback, squad_keyboard_callback


def make_invite_keyboard(ref_1: str, ref_2: str, status_invite: list):
    keyboard = InlineKeyboardMarkup(row_width=1)
    status_1, status_2 = status_invite[0], status_invite[1]
    ref_1_btn = InlineKeyboardButton(text=ref_1 + status_1,
                                     callback_data=invite_callback.new(
                                         data=ref_1+' '+ref_2, invite=ref_1, status=status_1))
    ref_2_btn = InlineKeyboardButton(text=ref_2 + status_2,
                                     callback_data=invite_callback.new(
                                         data=ref_1+' '+ref_2, invite=ref_2, status=status_2))
    back_btn = InlineKeyboardButton(text='<- Назад',
                                    callback_data=squad_keyboard_callback.new(user_id=0, phone='ver', ver='menu'))
    keyboard.insert(ref_1_btn)
    keyboard.insert(ref_2_btn)
    keyboard.insert(back_btn)
    return keyboard
