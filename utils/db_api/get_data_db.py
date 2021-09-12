import logging
from time import asctime

from loader import dp
from utils.db_api.connect import connection


async def get_invite(id_user):
    connect = await connection()
    try:
        with connect.cursor() as cursor:
            get_invite_db = "SELECT `ref_1`, `ref_2` FROM `users` WHERE `user_id`=%s  "
            cursor.execute(get_invite_db, id_user)
            list_invite = cursor.fetchone()
            ref_1 = list_invite.get('ref_1')
            ref_2 = list_invite.get('ref_2')
            connect.close()
            logging.info(f'Cоединение с БД закрыто')
            return ref_1, ref_2
    except Exception as ex:
        await dp.bot.send_message(id, f"Неизвестная ошибка{asctime}, напишите @badmajor об ошибке")
        logging.info(f'Не получилось записать пользователя... ошибка:{ex}')
        connect.close()
        logging.info(f'Cоединение с БД закрыто')
        return False


async def get_team_leader(id_user):
    """
    Выдает данные тимлидера
    """
    connect = await connection()
    try:
        with connect.cursor() as cursor:
            get_invite_db = "SELECT `id` FROM `users` WHERE `user_id`=%s  "
            cursor.execute(get_invite_db, id_user)
            id = cursor.fetchmany()[0].get('id')
            id_parent = id // 8
            get_data_invited_user = "SELECT `user_name`, `phone` FROM `users` WHERE `Id` = %s"
            cursor.execute(get_data_invited_user, id_parent)
            parent_data = cursor.fetchone()
            parent_user_name = parent_data.get('user_name')
            parent_phone = parent_data.get('phone')
            connect.close()
            return parent_user_name, parent_phone
    except Exception as ex:
        await dp.bot.send_message(id, f"Неизвестная ошибка{asctime}, напишите @badmajor об ошибке")
        logging.info(f'Не получилось записать пользователя... ошибка:{ex}')
        connect.close()
        logging.info(f'Cоединение с БД закрыто')
        return False


async def get_parent_data(message):
    """
    Выдает по чьему инвайту зареган юзер
    """
    connect = await connection()
    id = message.from_user.id
    try:
        with connect.cursor() as cursor:
            get_invite_db = "SELECT `id` FROM `users` WHERE `user_id`=%s  "
            cursor.execute(get_invite_db, id)
            id = cursor.fetchmany()[0].get('id')
            id_parent = id // 2
            get_data_invited_user = "SELECT `user_name`, `phone` FROM `users` WHERE `Id` = %s"
            cursor.execute(get_data_invited_user, id_parent)
            parent_data = cursor.fetchone()
            parent_user_name = parent_data.get('user_name')
            parent_phone = parent_data.get('phone')
            connect.close()
            return parent_user_name, parent_phone
    except Exception as ex:
        await dp.bot.send_message(id, f"Неизвестная ошибка{asctime}, напишите @badmajor об ошибке")
        logging.info(f'Не получилось записать пользователя... ошибка:{ex}')
        connect.close()
        logging.info(f'Cоединение с БД закрыто')
        return False


async def get_id(user_id):
    """
    Выдает id в БД по user_id
    """
    connect = await connection()
    try:
        with connect.cursor() as cursor:
            get_id_command = "SELECT `id` FROM `users` WHERE `user_id`=%s "
            cursor.execute(get_id_command, user_id)
            id_in_db = cursor.fetchone().get('id')
            connect.close()
            logging.info(f'Cоединение с БД закрыто')
            return id_in_db
    except Exception as ex:
        await dp.bot.send_message(user_id, f"Неизвестная ошибка, напишите @badmajor об ошибке")
        logging.info(f'Не получилось получить id... ошибка: {ex}')
        connect.close()
        logging.info(f'Cоединение с БД закрыто')
        return False


async def get_parent_id(invite):  # Переделать когда стану умнее
    """
    Выдает по чьему инвайту зареган юзер
    """
    connect = await connection()
    try:
        with connect.cursor() as cursor:
            get_id_command = "SELECT `id` FROM `users` WHERE (`ref_1`=%s OR `ref_2`=%s) "
            cursor.execute(get_id_command, (invite, invite))
            parent_id = cursor.fetchone().get('id')
            logging.info(f'Получил parent_id {parent_id}')
            connect.close()
            logging.info(f'Cоединение с БД закрыто')
            return parent_id
    except Exception as ex:
        logging.info(f'Не получилось записать пользователя... ошибка:{ex}')
        connect.close()
        logging.info(f'Cоединение с БД закрыто')
        return False


async def get_squad(id, n=3, squaq_list=None, id_in_db=None):
    if squaq_list is None:
        id_in_db = await get_id(id)
        squaq_list = []
    if n < 1:
        n = 3
        return
    for i in range(2):
        num = id_in_db * 2 + i
        squaq_list.append(num)
        await get_squad(id, n - 1, squaq_list, num)
    squaq_list.sort()
    return squaq_list


async def get_user_id(id_user_in_db):
    """
    Выдает user_id в БД по id
    """
    connect = await connection()
    try:
        with connect.cursor() as cursor:
            command = "SELECT `user_id` FROM `users` WHERE `Id`=%s "
            cursor.execute(command, id_user_in_db)
            id_in_db = cursor.fetchone().get('user_id')
            logging.info(f'Получил user_id {id_in_db}')
            connect.close()
            logging.info(f'Cоединение с БД закрыто')
            return id_in_db
    except Exception as ex:
        logging.info(f'Не получил user_id... ошибка: {ex}')
        connect.close()
        logging.info(f'Cоединение с БД закрыто')
        return False


async def get_user_data(id_user_in_db, db=True):
    """
    Если True - Выдает user_id, user_name и phone из БД по id
    Если False - Выдает id, user_name и phone из БД по user_id
    """
    connect = await connection()
    try:
        with connect.cursor() as cursor:
            if db:
                command = "SELECT `user_id`, `user_name`, `phone`, `verification`, `ref_1`, `ref_2` FROM `users` WHERE " \
                      "`Id`=%s "
            else:
                command = "SELECT `id`, `user_name`, `phone`, `verification`, `ref_1`, `ref_2` FROM `users` WHERE " \
                          "`user_id`=%s "
            cursor.execute(command, id_user_in_db)
            user_data_dict = cursor.fetchone()
            connect.close()
            logging.info(f'Cоединение с БД закрыто')
            return user_data_dict
    except Exception as ex:
        logging.info(f'Не получил user_data... ошибка: {ex}')
        connect.close()
        logging.info(f'Cоединение с БД закрыто')
        return False


async def get_3_line(user_id):
    """
    Выдает рефералов с третьей линии, списком словарей.
    """
    id_in_db = await get_id(user_id)
    first_ref = id_in_db * 2 ** 3
    list_ref_id = [first_ref + i for i in range(8)]
    list_dict_ref = []
    connect = await connection()
    try:
        with connect.cursor() as cursor:
            command = "SELECT `user_id`, `user_name`, `phone`, `verification` " \
                      "FROM `users` WHERE `Id`=%s "
            for user_id in list_ref_id:
                cursor.execute(command, user_id)
                tmp = cursor.fetchone()
                if tmp is not None:
                    list_dict_ref.append(tmp)
        connect.close()
        logging.info(f'Cоединение с БД закрыто')
        return list_dict_ref
    except Exception as ex:
        logging.info(f'Не получил user_data... ошибка: {ex}')
        connect.close()
        logging.info(f'Cоединение с БД закрыто')
        return False
