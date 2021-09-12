from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str
ADMINS = env.list("ADMINS")  # Тут у нас будет список из админов
BORN_LUCK = env.list('BORN_LUCK')  # Список тех кто имеет бесплатные инвайты
MYSQL_DB_NAME = env.str('MYSQL_DB_NAME')
MYSQL_DB_LOGIN = env.str('MYSQL_DB_LOGIN')
MYSQL_DB_PASSWORD = env.str('MYSQL_DB_PASSWORD')
SERVER_DB = env.str('SERVER_DB')