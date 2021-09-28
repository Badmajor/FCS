import logging
from loader import dp

from utils.db_api.connect import connection
from utils.db_api.get_data_db import get_parent_id
from utils.misc.generate_invite import create_invite


async def registration(message, data_user):
    """
        Вносит пользователя в БД
    """
    user_id = message.from_user.id
    invite = data_user.get('invite')
    phone = data_user.get('contact')
    name = message.from_user.username
    id_db = 0
    ver = 0
    parent_id = await get_parent_id(invite)
    if invite[-1] == 'r':
        id_db = parent_id * 2 + 1
    elif invite[-1] == 'l':
        id_db = parent_id * 2
    else:
        await dp.bot.send_message(user_id, "Ошибка регистрации, напишите @badmajor об ошибке")
    ref_1, ref_2 = await create_invite(id_db)
    connect = await connection()
    try:
        with connect.cursor() as cursor:
            command = "INSERT INTO `users`(`id`, `user_id`, `user_name`, `invite`, `phone`, `verification`, " \
                          "`ref_1`, `ref_2`) VALUE(%s, %s, %s, %s, %s, %s, %s, %s) "
            cursor.execute(command, (id_db, user_id, name, invite, phone, ver, 'fcs'+ref_1+'l', 'fcs'+ref_2+'r'))
            connect.commit()
            logging.info(f'Пользователь зарегистрирован {name}, {phone}')
            connect.close()
            logging.info(f'Cоединение с БД закрыто')
            return True
    except Exception as ex:
        await dp.bot.send_message(user_id, "Ошибка регистрации, напишите @badmajor об ошибке")
        logging.info(f'Не получилось записать пользователя... ошибка:{ex}')
        connect.close()
        logging.info(f'Cоединение с БД закрыто')
        return False



