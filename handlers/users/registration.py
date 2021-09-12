import logging
from aiogram import types
from aiogram.dispatcher import FSMContext, filters
from aiogram.dispatcher.filters import Command

from handlers.users.menu import start_menu
from loader import dp
from keyboards.default import get_contact_keyboard
from keyboards.inline.help_keyboard import help_keyboard
from states.RegistrationUser import RegistrationUser
from utils.db_api.check_input_data import check_invite, check_contact
from utils.db_api.check_status import check_status_user
from utils.db_api.registration_user_in_db import registration
from utils.help_command import help_command


@dp.message_handler(Command('reg'), state=None)
async def get_data_start(message: types.Message):
    status = await check_status_user(message.from_user.id)
    if status != 'no_reg':
        await start_menu(message)
        return
    await message.answer(f'Введи код приглашения. \n'
                         f'Начинается на "FCS"',
                         reply_markup=help_keyboard
                         )
    logging.info(f'{message.from_user.id} {message.from_user.username} Начинает регистрацию')
    await RegistrationUser.first()


@dp.message_handler(state=RegistrationUser.user_invite_state)
async def get_data_invite(message: types.Message, state: FSMContext):
    check = await check_invite(message.text.lower())
    if check:
        await state.update_data(invite=message.text.lower())  # обновление стейта
    elif message.text.lower() == '/:help':
        logging.info(f'{message.from_user.id}{message.from_user.username} Тыкает хэлп')
        await state.finish()
        await help_command(message)
    else:
        logging.info(f'{message.from_user.id}{message.from_user.username} {message.text.lower()} Ошибка инвайта')
        await message.answer('Код приглашения не верный! \n'
                             'Введите верный код (Начинается на "FCS")\n'
                             'Или нажмите на кнопку "Помощь"',
                             reply_markup=help_keyboard
                             )
        return
    await message.answer('Для продолжения регистрации, '
                         'мне нужен ваш номер телефона, '
                         'Все финансовые операции будут выполнять через него!'
                         '!!! ВАЖНО!!!'
                         'к телефону должна быть привязана карта Сбербанка.',
                         reply_markup=get_contact_keyboard)
    await RegistrationUser.user_contact_state.set()


@dp.message_handler(filters.IsSenderContact(True), content_types='contact', state=RegistrationUser.user_contact_state)
async def get_data_contact(message: types.Message, state: FSMContext):
    if not message.contact.phone_number:
        logging.info(f'{message.from_user.id}{message.from_user.username} Телефон не верный')
        await message.answer('Для продолжения регистрации, '
                             'мне нужен ваш номер телефона, '
                             'Все финансовые операции будут выполнять через него!'
                             '!!! ВАЖНО!!!'
                             'к телефону должна быть привязана карта Сбербанка.',
                             reply_markup=get_contact_keyboard)
        return
    check = await check_contact(message)
    if check:
        logging.info(f'{message.from_user.id}{message.from_user.username} Телефон верный')
        await state.update_data(contact=message.contact.phone_number)
        user_data = await state.get_data()
        reg_ok = await registration(message, user_data)
        if reg_ok:
            logging.info(f'{message.from_user.id}{message.from_user.username} Регистрация прошла успешно')
            await state.finish()
            await message.answer('Регистрация завершена.\n'
                                 'Перейдите в личный кабинет командой: /menu')
        else:
            logging.info(f'{message.from_user.id}{message.from_user.username} Ошибка регистрации')
            await state.finish()
            await message.answer('Неизвестная ошибка.\n'
                                 'Повторите регистрацию позже')
    else:
        logging.info(f'{message.from_user.id}{message.from_user.username} Телефон не верный')
        await message.answer('Для продолжения регистрации, '
                             'мне нужен ваш номер телефона, '
                             'Все финансовые операции будут выполнять через него!'
                             '!!! ВАЖНО!!!'
                             'к телефону должна быть привязана карта Сбербанка.',
                             reply_markup=get_contact_keyboard)
        return
