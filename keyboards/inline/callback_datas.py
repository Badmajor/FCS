from aiogram.utils.callback_data import CallbackData

help_callback = CallbackData('/', 'help')
menu_callback = CallbackData('menu', 'status', 'command')
squad_keyboard_callback = CallbackData('sq', 'user_id', 'phone', 'ver')
line3_callback = CallbackData('3l', 'user_id', 'phone', 'ver')
back_menu = CallbackData('menu', "back")
verification_callback = CallbackData('vr', 'ans')
invite_callback = CallbackData('invt', 'invite', 'status')