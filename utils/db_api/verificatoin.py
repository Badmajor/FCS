import asyncio
import logging

from keyboards.default.confirm_keyboards import confirm_verification_keyboard
from loader import bot, dp
from utils.db_api.connect import connection
from utils.db_api.get_data_db import get_user_data


async def confirm_verification(user_id, ref_id):
    msg = await bot.send_message(user_id, text='Верификацию отменить нельзя!')
    for i in range(6):
        if i < 5:
            await bot.edit_message_text(
                chat_id=msg.chat.id, message_id=msg.message_id,
                text=f'Верификацию отменить нельзя!\n'
                     f'5 секунд защита от случайного нажатия\n\n'
                     f'Обратный отсчет: {5 - i}')
        else:
            await bot.edit_message_text(
                chat_id=msg.chat.id, message_id=msg.message_id,
                text=f'Верификацию отменить нельзя!')
        await asyncio.sleep(1.0)
    data_ref_user = await get_user_data(ref_id, False)
    await bot.send_message(
        user_id, f'Верифицировать пользователя?\n'
                 f'@{data_ref_user.get("user_name")}', reply_markup=confirm_verification_keyboard)


async def edit_verification_status(ref_id, user_id):
    """
    Изменяет статус user в verification c 0 на 1
    """
    connect = await connection()
    try:
        with connect.cursor() as cursor:
            command = "UPDATE `users` SET `verification`=1 WHERE `user_id`=%s "
            cursor.execute(command, ref_id)
            connect.commit()
            logging.info(f'Пользователь верифицирован id: {ref_id}, LeaderSquad {user_id}')
            command = "UPDATE `users` SET `completed`=`completed` + 1 WHERE `user_id`=%s "
            cursor.execute(command, user_id)
            connect.commit()
            connect.close()
            logging.info(f'Cоединение с БД закрыто')
            return True
    except Exception as ex:
        await dp.bot.send_message(user_id, "Ошибка верификации, напишите @badmajor об ошибке")
        logging.info(f'Не получилось записать пользователя... ошибка:{ex}')
        connect.close()
        logging.info(f'Cоединение с БД закрыто')
        return False
