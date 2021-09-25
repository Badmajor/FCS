from contextlib import suppress

from aiogram.types import CallbackQuery
from aiogram.utils.exceptions import MessageNotModified

from keyboards.inline.callback_datas import invite_callback
from keyboards.inline.invite_keyboard import make_invite_keyboard
from loader import dp
from utils.db_api.check_status import check_status_invite


@dp.callback_query_handler(invite_callback.filter(), state='*')
async def send_invite(call: CallbackQuery, callback_data: dict):
    list_ref = list(callback_data.get("data").split(' '))
    ref_1, ref_2 = list_ref[0], list_ref[1]
    status_invite = [await check_status_invite(r) for r in [ref_1, ref_2]]
    if callback_data.get("status") == '🆓':
        await call.message.answer(callback_data.get("invite"))
        await call.message.answer(f'Перешлите это сообщение!\n'
                                  f'Код приглашения: {callback_data.get("invite")}\n'
                                  f'Ссылка на бота: @FreeCreditSquad_bot',
                                  reply_markup=make_invite_keyboard(ref_1, ref_2, status_invite))
    else:
        with suppress(MessageNotModified):
            await call.message.edit_text(f'Код приглашения уже занят.\n'
                                         f'🆓 - свободный\n'
                                         f'🆗 - занят',
                                         reply_markup=make_invite_keyboard(ref_1, ref_2, status_invite))
        await call.answer()
