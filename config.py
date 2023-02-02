import os
import logging.config
from dotenv import load_dotenv, find_dotenv
from logging_config import dict_config

if not find_dotenv():
    exit('Переменные окружения не загружены: проверьте файл .env')
else:
    load_dotenv()

BASE_URL = 'https://www.bestchange.ru/'
BOT_TOKEN = os.getenv('BOT_TOKEN')
logging.config.dictConfig(dict_config)
bot_logger = logging.getLogger('bot_logger')
parser_logger = logging.getLogger('parser_logger')
