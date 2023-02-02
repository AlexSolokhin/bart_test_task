from aiogram.utils import executor
from create_bot import dp
from config import bot_logger
import handlers


async def on_startup(_):
    bot_logger.info('Бот онлайн')


async def on_shutdown(_):
    bot_logger.info('Бот оффлайн')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)
