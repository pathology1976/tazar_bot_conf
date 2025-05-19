import os
from dotenv import load_dotenv
import logging
from logging.handlers import RotatingFileHandler
import pathlib

# Загрузка переменных окружения из .env файла
load_dotenv()

# Токен бота
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Список ID администраторов (преобразование строки с разделителями в список)
ADMIN_IDS = list(map(int, os.getenv('ADMIN_IDS', '').split(',')))

# Настройка путей
BASE_DIR = pathlib.Path(__file__).parent
DATA_DIR = BASE_DIR / 'data'
LOGS_DIR = BASE_DIR / 'logs'

# Создание директорий, если они не существуют
DATA_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# Путь к Excel-файлу
EXCEL_FILE = DATA_DIR / 'users.xlsx'

# Настройка логирования
def setup_logger():
    # Создаем логгер
    logger = logging.getLogger('bot_logger')
    logger.setLevel(logging.INFO)
    
    # Форматтер для логов
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Обработчик для файла с ротацией (максимум 5 файлов по 5 МБ)
    file_handler = RotatingFileHandler(
        LOGS_DIR / 'bot.log', 
        maxBytes=5*1024*1024,  # 5 МБ
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    
    # Обработчик для консоли
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # Добавляем обработчики к логгеру
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Инициализация логгера
logger = setup_logger()