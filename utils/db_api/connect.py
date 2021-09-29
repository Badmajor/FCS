import pymysql
from data.config import MYSQL_DB_NAME, MYSQL_DB_PASSWORD, MYSQL_DB_LOGIN, SERVER_DB
import logging


async def connection():
    try:
        connect = pymysql.connect(
            host=SERVER_DB,
            user=MYSQL_DB_LOGIN,
            password=MYSQL_DB_PASSWORD,
            database=MYSQL_DB_NAME,
            cursorclass=pymysql.cursors.DictCursor
        )
        logging.info(f'Подключились к БД успешно')
        return connect
    except Exception as ex:
        logging.info(f'Не получилось подключиться... ошибка:{ex}')



