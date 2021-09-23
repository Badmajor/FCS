from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

get_contact_keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
button_get_phone = KeyboardButton(text="Отправить номер телефона", request_contact=True)
button_cancel = KeyboardButton(text='Отмена')
get_contact_keyboard.add(button_get_phone)
get_contact_keyboard.add(button_cancel)