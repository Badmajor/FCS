import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from handlers.users.menu import start_menu, back_menu_reg
from keyboards.inline.callback_datas import menu_callback, verification_callback
from keyboards.inline.keybord_menu import keyboard_go_ver, keyboard_menu_registered_user
from keyboards.inline.line3_keyboard import line3_keyboard
from loader import dp, bot
from states.VerificationUser import VerificationUser
from states.view_list_user import ViewLine3
from utils.db_api.check_status import check_status_completed
from utils.db_api.delete_data_db import del_completed_account_db
from utils.db_api.get_data_db import get_3_line
from utils.db_api.verificatoin import edit_verification_status


@dp.message_handler(state=ViewLine3.verification_user)
async def verification(message: types.Message, state: FSMContext):
    if message.text.lower() == 'подтвердить!':
        data = await state.get_data()
        ref_id = data.get("ref_id")
        user_id = message.from_user.id
        if await edit_verification_status(ref_id, user_id):
            await message.answer(f'Верификация прошла успешно!', reply_markup=types.ReplyKeyboardRemove())
            await bot.send_message(ref_id, 'Вас верифицировали.\n Мои поздравления!\n\n'
                                           'Используйте команду /menu для перехода в личный кабинет')
            completed = await check_status_completed(user_id)
            if completed >= 8:
                await message.answer('Вы только что закрыли сквад, Поздравляю\n'
                                     'Ваши данные удалены из базы данных\n'
                                     'Вы можете снова пройти регистрацию. Код приглашения можно попросить у друзей')
                await del_completed_account_db(message)
        else:
            logging.info(f'Верификация user_id: {ref_id} не прошла')
        await state.finish()
        await start_menu(message)

    else:
        list_dict_ref = await get_3_line(message.from_user.id)
        await message.answer(f'список рефов третьей линии get_3_line',
                             reply_markup=line3_keyboard(list_dict_ref))
        await ViewLine3.user_view_state.set()


@dp.callback_query_handler(menu_callback.filter(), state=VerificationUser.user_call_state)
async def go_verification(call: CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data.get('command') == 'go_ver':
        leader_data = await state.get_data()
        await call.message.edit_text(f'Шаг 1 из 3\n\n'
                                     f'Свяжитесь с SquadLeader и уточните реквизиты\n'
                                     f'@{leader_data.get("squadleader")}\n'
                                     f'{leader_data.get("phoneleader")}', reply_markup=keyboard_go_ver)
        await VerificationUser.next()
    else:
        await state.finish()
        await back_menu_reg(call)


@dp.callback_query_handler(verification_callback.filter(), state=VerificationUser.user_pay_state)
async def go_verification_step2(call: CallbackQuery, callback_data: dict, state: FSMContext):
    leader_data = await state.get_data()
    if callback_data.get('ans') == 'ok':
        await call.message.edit_text(f'Шаг 2 из 3\n\n'
                                     f'Отправьтe деньги @{leader_data.get("squadleader")}\n',
                                     reply_markup=keyboard_go_ver)
        await VerificationUser.next()
    elif callback_data.get('ans') == 'fail':
        await state.finish()
        logging.info(f"User: {call.message.from_user.username}, id: {call.message.from_user.id} "
                     f"Не смог связаться с {leader_data}")
        await call.message.edit_text(f'Попробуйте связаться позднее\n\n'
                                     f'Если @{leader_data.get("squadleader")} не ответить\n'
                                     f'Напишите @Badmajor',
                                     reply_markup=keyboard_menu_registered_user)
    else:
        await state.finish()
        await back_menu_reg(call)


@dp.callback_query_handler(verification_callback.filter(), state=VerificationUser.user_send_pay_data_state)
async def go_verification_step3(call: CallbackQuery, callback_data: dict, state: FSMContext):
    leader_data = await state.get_data()
    if callback_data.get('ans') == 'ok':
        await call.message.edit_text(f'Шаг 3 из 3\n\n'
                                     f'Отправьте чек @{leader_data.get("squadleader")}\n'
                                     f'Обязательно сохраните чек до конца верификации',
                                     reply_markup=keyboard_go_ver)
        await VerificationUser.next()
        await bot.send_message(leader_data.get("user_id"), f'Пользователь {call.from_user.username}'
                                                           f'отправил Вам деньги. Проверьте поступление средств и '
                                                           f'верифицируйте пользователя.')
    elif callback_data.get('ans') == 'fail':
        await state.finish()
        logging.info(f"User: {call.message.from_user.username}, id: {call.message.from_user.id} "
                     f"Не смог отправить деньги {leader_data}")
        await call.message.edit_text(f'Попробуйте позднее\n\n'
                                     f'или свяжитесь  с @{leader_data.get("squadleader")}\n',
                                     reply_markup=keyboard_menu_registered_user)
    else:
        await state.finish()
        await back_menu_reg(call)


@dp.callback_query_handler(verification_callback.filter(), state=VerificationUser.finish_state)
async def go_verification_finish(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await back_menu_reg(call)
