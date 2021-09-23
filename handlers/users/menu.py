from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.default.confirm_keyboards import confirm_verification_keyboard
from keyboards.inline.keybord_menu import keyboard_menu_verified_user, keyboard_menu_registered_user

from loader import dp
from states.RegistrationUser import RegistrationUser
from states.VerificationUser import VerificationUser
from utils.db_api.check_status import check_status_user, check_status_invite
from utils.db_api.delete_data_db import del_account_db
from utils.db_api.get_data_db import get_parent_data, get_team_leader, get_invite


@dp.message_handler(commands="menu")
async def start_menu(message: types.Message):
    status = await check_status_user(message.from_user.id)
    if status == 'ver':
        await message.answer(f'Личный кабинет\n\n'
                             f'Вы всегда можете помочь своей команде!'
                             f'Посмотреть Коды приглашений вашего Squad\n'
                             f'сможете в профиле.', reply_markup=keyboard_menu_verified_user)
    elif status == 'reg':
        invited_name, phone = await get_parent_data(message.from_user.id)
        if '+' not in phone:
            phone = '+' + phone
        await message.answer(f'Ваш аккаунт не верифицирован!\n'
                             f'Подробнее: ссылка на гайд по вериф.\n\n'
                             f'Вас пригласил: @{invited_name} \n'
                             f'Контакт: {phone}', reply_markup=keyboard_menu_registered_user)
    else:
        await message.answer('Для регисрации используй команду /reg')


@dp.callback_query_handler(text_contains='reg:menu')
async def back_menu_reg(call: CallbackQuery):
    invited_name, phone = await get_parent_data(call.from_user.id)
    if '+' not in phone:
        phone = '+' + phone
    await call.message.edit_text(f'Ваш аккаунт не верифицирован!\n'
                                 f'Подробнее: ссылка на гайд по вериф.\n\n'
                                 f'Вас пригласил: @{invited_name} \n'
                                 f'Контакт: {phone}', reply_markup=keyboard_menu_registered_user)


@dp.callback_query_handler(text_contains='ver:menu')
async def back_menu_ver(call: CallbackQuery):
    await call.message.edit_text(f'Личный кабинет \n\n'
                                 f'Вы всегда можете помочь своей команде!'
                                 f'Посмотреть Коды приглашений вашего Squad\n'
                                 f'сможете в профиле.', reply_markup=keyboard_menu_verified_user)


@dp.callback_query_handler(text_contains='ver:invite')
async def view_invite_list(call: CallbackQuery):
    await call.answer(cache_time=5)
    ref_1, ref_2 = await get_invite(call.from_user.id)
    status_invite = [await check_status_invite(r) for r in [ref_1, ref_2]]
    await call.message.edit_text(f'Коды приглашения:\n'
                                 f'{ref_1} - {status_invite[0]}\n'
                                 f'{ref_2} - {status_invite[1]}',
                                 reply_markup=keyboard_menu_verified_user)


@dp.callback_query_handler(text_contains='ver:info')
async def view_info(call: CallbackQuery):
    await call.answer(cache_time=5)
    await call.message.edit_text('типа показываю больше инфо',
                                 reply_markup=keyboard_menu_verified_user)


@dp.callback_query_handler(text_contains='reg:info')
async def view_info(call: CallbackQuery):
    await call.answer(cache_time=5)
    await call.message.edit_text('типа показываю больше инфо',
                                 reply_markup=keyboard_menu_registered_user)


@dp.callback_query_handler(text_contains='reg:go_ver', state=None)
async def go_verification(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=2)
    status = await check_status_user(call.from_user.id)
    if status == 'ver':
        await call.message.edit_text(f'Вы прошли верификацию\n'
                                     f'Вам осталось пригласить 2 друзей\n'
                                     f'и смотреть как растет ваш Squad',
                                     reply_markup=keyboard_menu_verified_user)
    else:
        squadleader, phone, sq_user_id = await get_team_leader(call.from_user.id)
        if '+' not in phone:
            phone = '+' + phone
        await call.message.edit_text(f'Ваш SquadLeader: @{squadleader}\n'
                                     f'Номер для перевода: {phone}\n\n'
                                     f'Перед отправкой денег свяжитесь с Тилидером.\n'
                                     f'После отпраки денег сохраните информацию о платеже'
                                     f'и напомните, что бы Вас верифицировали',
                                     reply_markup=keyboard_menu_registered_user)
        await state.update_data(squadleader=squadleader, phoneleader=phone, user_id=sq_user_id)
        await VerificationUser.first()


@dp.callback_query_handler(text_contains='reg:del', state=None)
async def del_account_call(call: CallbackQuery):
    await call.answer(cache_time=5)
    await call.message.answer('Удалить аккаунт?', reply_markup=confirm_verification_keyboard)
    await RegistrationUser.user_del_account.set()


@dp.message_handler(state=RegistrationUser.user_del_account)
async def del_account(message: types.Message, state: FSMContext):
    if message.text.lower() == 'подтвердить!':
        if await del_account_db(message):
            await message.answer('Аккаунт удален!\n'
                                 'Вы всегда можете зарегистрироваться еще раз!')
        await state.finish()
        await start_menu(message)
    else:
        await state.finish()
        await start_menu(message)
