import logging

from utils.db_api.connect import connection


async def auto_create_user(list_id: list):
    connect = await connection()
    with connect.cursor() as cursor:
        command = "INSERT INTO `users`(`id`, `user_id`, `user_name`, `invite`, `phone`, `verification`, " \
                  "`ref_1`, `ref_2`) VALUE(%s, %s, %s, %s, %s, %s, %s, %s) "
        for id in list_id:
            n = 8 + id
            ver = 0
            if n % 2:
                ver = 1
            cursor.execute(command, (id, n, 'fcs'+str(n), 'fcs'+str(n), '+79625663355',
                                     ver, 'fcs'+str(n)+'l', 'fcs'+str(n)+'r'))
            connect.commit()
            logging.info(f'Пользователь зарегистрирован {n}, {ver}')
        connect.close()
