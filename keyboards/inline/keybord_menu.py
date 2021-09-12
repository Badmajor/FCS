from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import menu_callback

keyboard_menu_verified_user = InlineKeyboardMarkup(row_width=2)  # row_width это длина клавиатуры в кнопках

view_squad = InlineKeyboardButton(text='Мой Squad', callback_data=menu_callback.new(
    status='ver', command='squad'))
view_info = InlineKeyboardButton(text='Инфо', callback_data=menu_callback.new(
    status='ver', command='info'))
view_invite = InlineKeyboardButton(text='Пригласить', callback_data=menu_callback.new(
    status='ver', command='invite'))
ver_pay = InlineKeyboardButton(text='Подтвердить', callback_data=menu_callback.new(
    status='ver', command='ver'))


keyboard_menu_verified_user.insert(view_squad)
keyboard_menu_verified_user.insert(view_info)
keyboard_menu_verified_user.insert(view_invite)
keyboard_menu_verified_user.insert(ver_pay)

keyboard_menu_verified_user.add(InlineKeyboardButton(
        text='<- Назад',callback_data=menu_callback.new(status='ver', command='main')))

keyboard_menu_registered_user = InlineKeyboardMarkup(row_width=2)  # row_width это длина клавиатуры в кнопках

del_btn = InlineKeyboardButton(text='Удалить аккаунт', callback_data=menu_callback.new(
    status='reg', command='del'))
view_info = InlineKeyboardButton(text='Инфо', callback_data=menu_callback.new(
    status='reg', command='info'))
ver_btn = InlineKeyboardButton(text='Пройти верификацию', callback_data=menu_callback.new(
    status='reg', command='go_ver'))

keyboard_menu_registered_user.insert(del_btn)
keyboard_menu_registered_user.insert(view_info)
keyboard_menu_registered_user.insert(ver_btn)

keyboard_menu_registered_user.add(InlineKeyboardButton(
        text='<- Назад',callback_data=menu_callback.new(status='ver', command='main')))