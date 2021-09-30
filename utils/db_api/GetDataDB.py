import logging

import pymysql

from data.config import SERVER_DB, MYSQL_DB_LOGIN, MYSQL_DB_PASSWORD, MYSQL_DB_NAME


class GetDataUser:
    """
    Выдает даннык из БД
    """

    def __init__(self, user_id):
        connect = pymysql.connect(
            host=SERVER_DB,
            user=MYSQL_DB_LOGIN,
            password=MYSQL_DB_PASSWORD,
            database=MYSQL_DB_NAME,
            cursorclass=pymysql.cursors.DictCursor)
        with connect.cursor() as cursor:
            command = "SELECT `id`, `user_name`, `invite`, `phone`, `verification`, `ref_1`, `ref_2`, `completed` " \
                      "FROM `users` WHERE `user_id`=%s "
            cursor.execute(command, user_id)
            self.data = cursor.fetchone()
        connect.close()
        logging.info(f'Cоединение с БД закрыто')

    def id(self):
        return self.data.get('id')

    def user_name(self):
        return self.data.get('user_name')

    def invite(self):
        return self.data.get('invite')

    def phone(self):
        return self.data.get('phone')

    def verification(self):
        return self.data.get('verification')

    def ref_1(self):
        return self.data.get('ref_1')

    def ref_2(self):
        return self.data.get('ref_2')

    def completed(self):
        return self.data.get('completed')
