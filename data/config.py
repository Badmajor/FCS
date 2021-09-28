import os

from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = os.environ["BOT_TOKEN"]  # Забираем значение типа str
ADMINS = os.environ["ADMINS"]  # Тут у нас будет список из админов

MYSQL_DB_NAME = os.environ['MYSQL_DB_NAME']
MYSQL_DB_LOGIN = os.environ['MYSQL_DB_LOGIN']
MYSQL_DB_PASSWORD = os.environ['MYSQL_DB_PASSWORD']
SERVER_DB = os.environ['SERVER_DB']

WEBHOOK_HOST = os.environ['WEBHOOK_HOST']
WEBHOOK_PATH = os.environ['WEBHOOK_PATH']
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"
WEBAPP_HOST = os.environ['WEBAPP_HOST']
WEBAPP_PORT = os.environ.get('PORT')
