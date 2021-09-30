import logging
from time import asctime

from loader import dp
from utils.db_api.GetDataDB import GetDataUser
from utils.db_api.connect import connection


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
            get_data_invited_user = "SELECT `user_name`, `phone`, `user_id` FROM `users` WHERE `Id` = %s"
            cursor.execute(get_data_invited_user, id_parent)
            leader_data = cursor.fetchone()
            leader_user_name = leader_data.get('user_name')
            leader_phone = leader_data.get('phone')
            leader_user_id = leader_data.get('user_id')
            connect.close()
            return leader_user_name, leader_phone, leader_user_id
    except Exception as ex:
        await dp.bot.send_message(id, f"Неизвестная ошибка{asctime}, напишите @badmajor об ошибке")
        logging.info(f'Не получилось записать пользователя... ошибка:{ex}')
        connect.close()
        logging.info(f'Cоединение с БД закрыто')
        return False


async def get_parent_data(user_id):
    """
    Выдает по чьему инвайту зареган юзер
    """
    connect = await connection()
    try:
        with connect.cursor() as cursor:
            get_invite_db = "SELECT `id` FROM `users` WHERE `user_id`=%s  "
            cursor.execute(get_invite_db, user_id)
            id = cursor.fetchone().get('id')

            id_parent = id // 2
            get_data_invited_user = "SELECT `user_name`, `phone` FROM `users` WHERE `Id` = %s"
            cursor.execute(get_data_invited_user, id_parent)
            parent_data = cursor.fetchone()
            parent_user_name = parent_data.get('user_name')
            parent_phone = parent_data.get('phone')
            connect.close()
            logging.info(f'Cоединение с БД закрыто')
            return parent_user_name, parent_phone
    except Exception as ex:
        await dp.bot.send_message(user_id, f"Неизвестная ошибка{asctime}, напишите @badmajor об ошибке")
        logging.info(f'Не получилось записать пользователя... ошибка:{ex}')
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


async def get_list_id_squad_3_line(id, n=3, squaq_list=None, id_in_db=None):
    """
    Выдает всех рефов, списком по id до 3 линии
    """
    if squaq_list is None:
        user = GetDataUser(id)
        id_in_db = user.id()
        squaq_list = []
    if n < 1:
        return
    for i in range(2):
        num = id_in_db * 2 + i
        squaq_list.append(num)
        await get_list_id_squad_2_line(id, n - 1, squaq_list, num)
    squaq_list.sort()
    return squaq_list


async def get_list_id_squad_2_line(id, n=2, squaq_list=None, id_in_db=None):
    """
    Выдает всех рефов, списком по id до 2 линии
    """
    if squaq_list is None:
        user = GetDataUser(id)
        id_in_db = user.id()
        squaq_list = []
    if n < 1:
        return
    for i in range(2):
        num = id_in_db * 2 + i
        squaq_list.append(num)
        await get_list_id_squad_2_line(id, n - 1, squaq_list, num)
    squaq_list.sort()
    return squaq_list


async def get_data_user_list(list_user_id: list):
    list_dict_ref = []
    connect = await connection()
    try:
        with connect.cursor() as cursor:
            command = "SELECT `user_id`, `user_name`, `phone`, `verification` " \
                      "FROM `users` WHERE `Id`=%s "
            for user_id in list_user_id:
                cursor.execute(command, user_id)
                tmp = cursor.fetchone()
                list_dict_ref.append(tmp)
        connect.close()
        logging.info(f'Cоединение с БД закрыто')
        return list_dict_ref
    except Exception as ex:
        logging.info(f'Не получил user_data... ошибка: {ex}')
        connect.close()
        logging.info(f'Cоединение с БД закрыто')
        return False


async def get_3_line(user_id):
    """
    Выдает рефералов с третьей линии, списком словарей.
    """
    user = GetDataUser(user_id)
    id_in_db = user.id()
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
