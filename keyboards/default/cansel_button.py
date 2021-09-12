from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

cansel_button_keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
cansel_button = KeyboardButton(text="Отменить регистрацию")
cansel_button_keyboard.add(cansel_button)