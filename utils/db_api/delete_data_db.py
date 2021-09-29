import logging

from loader import dp
from utils.db_api.connect import connection


async def del_account_db(message):
    user_id = message.from_user.id
    connect = await connection()
    try:
        with connect.cursor() as cursor:
            command = "DELETE FROM `users` WHERE `user_id`=%s"
            cursor.execute(command, user_id)
            connect.commit()
            logging.info(f'Пользователь Удален. user захотел {user_id}')
            connect.close()
            logging.info(f'Cоединение с БД закрыто')
            return True
    except Exception as ex:
        await dp.bot.send_message(user_id, "Ошибка регистрации, напишите @badmajor об ошибке")
        logging.info(f'Не получилось удалить пользователя... ошибка:{ex}')
        connect.close()
        logging.info(f'Cоединение с БД закрыто')
        return False


async def del_completed_account_db(message):
    user_id = message.from_user.id
    connect = await connection()
    try:
        with connect.cursor() as cursor:
            command = "UPDATE `users` SET `user_id`=777, `invite`=0, `ref_1` = 0, " \
                      "`ref_2`=0 WHERE `user_id`=%s "
            cursor.execute(command, user_id)
            connect.commit()
            logging.info(f'Пользователь Удален. Squad copleted {user_id}')
            connect.close()
            logging.info(f'Cоединение с БД закрыто')
            return True
    except Exception as ex:
        await dp.bot.send_message(user_id, "Ошибка регистрации, напишите @badmajor об ошибке")
        logging.info(f'Не получилось удалить пользователя... ошибка:{ex}')
        connect.close()
        logging.info(f'Cоединение с БД закрыто')
        return False
