from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

confirm_verification_keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
button_confirm = KeyboardButton(text="Подтвердить!")
button_cancel = KeyboardButton(text='Отмена')
confirm_verification_keyboard.insert(button_confirm)
confirm_verification_keyboard.insert(button_cancel)
