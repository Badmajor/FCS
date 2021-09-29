import asyncio
import logging

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from handlers.users.menu import back_menu_ver, view_invite_list
from keyboards.inline.callback_datas import squad_keyboard_callback, line3_callback
from keyboards.inline.invite_keyboard import make_invite_keyboard
from keyboards.inline.keybord_menu import keyboard_menu_verified_user
from keyboards.inline.line3_keyboard import line3_keyboard, line3_keyboard_ver
from keyboards.inline.squad_keyboard import make_squad_keyboard
from loader import dp
from states.view_list_user import ViewLine3, ViewSquad
from utils.db_api.check_status import check_status_invite
from utils.db_api.get_data_db import get_3_line, get_list_id_squad_2_line, get_data_user_list, get_invite
from utils.db_api.verificatoin import confirm_verification


@dp.callback_query_handler(text_contains='ver:squad')
async def view_squad(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=5)
    list_squad_id = await get_list_id_squad_2_line(call.from_user.id)
    list_squad = await get_data_user_list(list_squad_id)
    await state.update_data(list_dict_ref=list_squad)
    if list_squad:
        await call.message.edit_text(f'Ваш squad\n\n'
                                     f'Если есть люди желающие вступить в FCS,\n'
                                     f'но у вас кончились коды приглашения\n'
                                     f'всегда можете позаимствовать их у членов своего Squad.\n'
                                     f'Для этого перейдите в профиль пользователя',
                                     reply_markup=make_squad_keyboard(list_squad))
        await ViewSquad.user_view_state.set()
    else:
        await call.message.edit_text(f'Ваш squad пуст\n'
                                     f'Вы еще никого не пригласили',
                                     reply_markup=keyboard_menu_verified_user)
        await asyncio.sleep(2.5)
        await state.finish()
        await view_invite_list(call)


@dp.callback_query_handler(squad_keyboard_callback.filter(), state=ViewSquad.user_view_state)
async def view_squad_user(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=5)
    if callback_data.get('ver') == 'menu':
        await state.finish()
        await back_menu_ver(call)
        return
    ref_1, ref_2 = await get_invite(callback_data.get('user_id'))
    status_invite = [await check_status_invite(r) for r in [ref_1, ref_2]]
    list_squad = await state.get_data('list_squad')
    if callback_data.get('ver') == '1':
        await call.message.answer(
            f'{callback_data.get("phone")} \nПрошел верификацию!\n\n'
            f'Коды приглашений:\n'
            f'{ref_1} - {status_invite[0]}\n'
            f'{ref_2} - {status_invite[1]}',
            reply_markup=make_invite_keyboard(ref_1, ref_2, status_invite)
        )
    else:
        await call.message.edit_text(
            f'{callback_data.get("phone")} \nНе прошел верификацию!',
            reply_markup=make_squad_keyboard(list_squad.get('list_dict_ref'))
        )


@dp.callback_query_handler(text_contains='ver:ver')
async def view_3line_ref(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=5)
    list_dict_ref = await get_3_line(call.from_user.id)
    await state.update_data(list_dict_ref=list_dict_ref)
    await call.message.edit_text(f'список рефов третьей линии get_3_line',
                                 reply_markup=line3_keyboard(list_dict_ref))
    await ViewLine3.user_view_state.set()


@dp.callback_query_handler(line3_callback.filter(), state=ViewLine3.user_view_state)
async def view_line3_user(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=5)
    if callback_data.get('ver') == 'menu':
        await state.finish()
        await back_menu_ver(call)
        return
    if callback_data.get('ver') == 'go_pay':
        ref_id = call.data.split(':')[1]
        user_id = call.from_user.id
        await confirm_verification(user_id, ref_id)
        await state.update_data(ref_id=ref_id)
        await ViewLine3.verification_user.set()
    list_dict_ref = await state.get_data('list_dict_ref')
    try:
        if callback_data.get('ver') == '1':
            await call.message.edit_text(
                f'{callback_data.get("phone")} \nПрошел верификацию!',
                reply_markup=line3_keyboard(list_dict_ref.get('list_dict_ref'))
            )
        else:
            await call.message.edit_text(
                f'{callback_data.get("phone")} \nНе прошел верификацию!',
                reply_markup=line3_keyboard_ver(list_dict_ref.get('list_dict_ref', ), call)
            )
    except Exception as ex:
        logging.info(f'... ошибка: {ex}')


@dp.callback_query_handler(line3_callback.filter(), state=None)
async def skip(call: CallbackQuery):
    await back_menu_ver(call)
