import logging

from loader import dp
from utils.db_api.connect import connection


async def check_status_user(id):
    """
    Проверяет зарегистрирован ли пользователь. Возвращает 'no_reg', 'reg' и 'ver' соответственно
    """
    flag = 'no_reg'
    connect = await connection()
    try:
        with connect.cursor() as cursor:
            command_db = "SELECT * FROM `users`  "
            cursor.execute(command_db)
            rows = cursor.fetchall()
            for row in rows:
                if id == row.get('user_id'):
                    flag = 'reg'
                    if row.get('verification') > 0:
                        flag = 'ver'
                        break
                    else:
                        break
            connect.close()
            logging.info(f'Cоединение с БД закрыто')
            return flag
    except Exception as ex:
        await dp.bot.send_message(id, "Не удалось проверить статус напишите @badmajor об ошибке")
        logging.info(f'Не удалось проверить статус пользователя... ошибка:{ex}')
        connect.close()
        logging.info(f'Cоединение с БД закрыто')
        return flag


async def check_status_invite(ref):
    """
    Проверяет зарегистрирован ли пользователь. Возвращает 'no_reg', 'reg' и 'ver' соответственно
    """
    connect = await connection()
    try:
        with connect.cursor() as cursor:
            command = "SELECT `invite` FROM `users`  "
            cursor.execute(command)
            rows = cursor.fetchall()
            connect.close()
            for row in rows:
                if ref in row.get('invite'):
                    logging.info(f'Cоединение с БД закрыто')
                    return '🆗'
            logging.info(f'Cоединение с БД закрыто')
            return '🆓'
    except Exception as ex:
        await dp.bot.send_message(id, "Не удалось проверить статус напишите @badmajor об ошибке")
        logging.info(f'Не удалось проверить статус пользователя... ошибка:{ex}')
        connect.close()
        logging.info(f'Cоединение с БД закрыто')


async def check_status_completed(user_id):
    """
    Проверяет сколько верификаций провел user. Return int
    """
    connect = await connection()
    try:
        with connect.cursor() as cursor:
            command = "SELECT `completed` FROM `users` WHERE user_id=%s "
            cursor.execute(command, user_id)
            completed = cursor.fetchone().get('completed')
            connect.close()
            logging.info(f'Cоединение с БД закрыто')
            return completed
    except Exception as ex:
        await dp.bot.send_message(user_id, "Не удалось проверить статус 'Completed', напишите @badmajor об ошибке")
        logging.info(f'Не удалось проверить статус пользователя... ошибка:{ex}')
        connect.close()
        logging.info(f'Cоединение с БД закрыто')
