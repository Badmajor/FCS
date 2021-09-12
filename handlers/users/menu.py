import logging

from aiogram import types
from aiogram.types import CallbackQuery

from keyboards.inline.keybord_menu import keyboard_menu_verified_user, keyboard_menu_registered_user
from keyboards.inline.line3_keyboard import line3_keyboard
from keyboards.inline.squad_keyboard import make_squad_keyboard
from loader import dp
from utils.db_api.auto_create import auto_create_user
from utils.db_api.check_input_data import check_status_completed
from utils.db_api.check_status import check_status_user, check_status_invite
from utils.db_api.get_data_db import get_parent_data, get_team_leader, get_invite, get_squad, get_user_id, \
    get_user_data, get_3_line


@dp.message_handler(commands="menu")
async def start_menu(message: types.Message):
    status = await check_status_user(message.from_user.id)
    if status == 'ver':
        await message.answer(f'Личный кабинет\n\n'
                             f'Вы всегда можете помочь своей команде!', reply_markup=keyboard_menu_verified_user)
    elif status == 'reg':
        invited_name, phone = await get_parent_data(message)
        if '+' not in phone:
            phone = '+' + phone
        await message.answer(f'Ваш аккаунт не верифицирован!\n'
                             f'Подробнее: ссылка на гайд по вериф.\n\n'
                             f'Вас пригласил: @{invited_name} \n'
                             f'Контакт: {phone}', reply_markup=keyboard_menu_registered_user)
    else:
        await message.answer('Для регисрации используй команду /reg')


@dp.callback_query_handler(text_contains='ver:main')
async def back_menu(call: CallbackQuery):
    await call.message.edit_text(f'Личный кабинет \n\n'
                                 f'Вы всегда можете помочь своей команде!',
                                 reply_markup=keyboard_menu_verified_user)


@dp.callback_query_handler(text_contains='ver:squad')
async def view_squad(call: CallbackQuery):
    await call.answer(cache_time=5)
    list_squad = []
    for id in await get_squad(call.from_user.id):
        tmp = await get_user_data(id)
        if tmp:
            list_squad.append(tmp)
        else:
            break
    await call.message.edit_text(f'Ваш squad'
                                 f'',
                                 reply_markup=make_squad_keyboard(list_squad))


@dp.callback_query_handler(text_contains='ver:invite')
async def view_squad(call: CallbackQuery):
    await call.answer(cache_time=5)
    ref_1, ref_2 = await get_invite(call.from_user.id)
    status_invite = [await check_status_invite(r) for r in [ref_1, ref_2]]
    await call.message.edit_text(f'Коды приглашения:\n'
                                 f'{ref_1} - {status_invite[0]}\n'
                                 f'{ref_2} - {status_invite[0]}',
                                 reply_markup=keyboard_menu_verified_user)


@dp.callback_query_handler(text_contains='ver:ver')
async def view_squad(call: CallbackQuery):
    await call.answer(cache_time=5)
    list_dict_ref = await get_3_line(call.from_user.id)
    await call.message.edit_text(f'список рефов третьей линии get_3_line{list_dict_ref}',
                                 reply_markup=line3_keyboard(list_dict_ref))


@dp.callback_query_handler(text_contains='ver:info')
async def view_squad(call: CallbackQuery):
    await call.answer(cache_time=5)
    await call.message.edit_text('типа показываю больше инфо',
                                 reply_markup=keyboard_menu_verified_user)


@dp.callback_query_handler(text_contains='reg:info')
async def view_squad(call: CallbackQuery):
    await call.answer(cache_time=5)
    await call.message.edit_text('типа показываю больше инфо',
                                 reply_markup=keyboard_menu_registered_user)


@dp.callback_query_handler(text_contains='reg:go_ver')
async def view_squad(call: CallbackQuery):
    await call.answer(cache_time=5)
    teamleader, phone = await get_team_leader(call.from_user.id)
    if '+' not in phone:
        phone = '+' + phone
    status = await check_status_user(call.from_user.id)
    if status == 'ver':
        await call.message.edit_text(f'Вы прошли верификацию\n'
                                     f'Вам осталось пригласить 2 друзей\n'
                                     f'и смотреть как рfстет ваш Squad',
                                     reply_markup=keyboard_menu_verified_user)
    else:
        await call.message.edit_text(f'Ваш Тимлидер: @{teamleader}\n'
                                     f'Номер для перевода: {phone}\n\n'
                                     f'Перед отправкой денег свяжитесь с Тилидером.\n'
                                     f'После отпраки денег сохраните информацию о платеже'
                                     f'и напомните, что бы Вас верифицировали',
                                     reply_markup=keyboard_menu_registered_user)


@dp.callback_query_handler(text_contains='reg:del')
async def view_squad(call: CallbackQuery):
    await call.answer(cache_time=5)
    await call.message.edit_text('типа удалил аккаунт',
                                 reply_markup=keyboard_menu_registered_user)
