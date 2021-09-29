import logging

from aiogram import types

from keyboards.default import get_contact_keyboard
from utils.db_api.connect import connection


async def check_invite(invite):
    """
    Проверяет актуальность инвайта
    """
    connect = await connection()
    try:
        with connect.cursor() as cursor:
            list_busy_invite = "SELECT `invite` FROM `users` "
            cursor.execute(list_busy_invite)
            rows_b = cursor.fetchall()
            for row_b in rows_b:
                if invite in row_b.get('invite'):
                    logging.info(f'Ввели использованый инвайт')
                    connect.close()
                    logging.info(f'Cоединение с БД закрыто')
                    return False
            list_free_invite = "SELECT `ref_1`, `ref_2` FROM `users` "
            cursor.execute(list_free_invite)
            rows_f = cursor.fetchall()
            for row_f in rows_f:
                if invite in list(row_f.values()):
                    logging.info(f'Ввели верный инвайт')
                    connect.close()
                    logging.info(f'Cоединение с БД закрыто')
                    return True
            connect.close()
            logging.info(f'Cоединение с БД закрыто')
            return False
    except Exception as ex:
        logging.info(f'Не получилось записать пользователя... ошибка:{ex}')
        connect.close()
        logging.info(f'Cоединение с БД закрыто')
        return False


async def check_contact(message):
    user_id = message.from_user.id
    id_in_message = message.contact.user_id
    if id_in_message == user_id:
        await message.answer('Номер телефона добавлен', reply_markup=types.ReplyKeyboardRemove())
        return True
    else:
        await message.answer('Нужно отправить номер который привязан к Telegram', reply_markup=get_contact_keyboard)
