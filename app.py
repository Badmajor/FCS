
from aiogram.utils.executor import start_webhook

from data.config import WEBHOOK_URL, WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT
from loader import dp, bot
import middlewares, filters, handlers
from utils import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    await bot.set_webhook(WEBHOOK_URL)
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    start_webhook(dispatcher=dp, webhook_path=WEBHOOK_PATH,
                  on_startup=on_startup, skip_updates=True,
                  host=WEBAPP_HOST, port=WEBAPP_PORT)
