import pandas as pd
import os
from datetime import datetime
import pytz
from config import EXCEL_FILE, logger

def save_user_data(user_data: dict) -> bool:
    """
    Сохраняет данные пользователя в Excel-файл.
    
    Args:
        user_data: Словарь с данными пользователя
        
    Returns:
        bool: True если сохранение успешно, иначе False
    """
    try:
        # Добавляем дату и время (Москва, UTC+3)
        moscow_tz = pytz.timezone('Europe/Moscow')
        now = datetime.now(moscow_tz)
        user_data['datetime'] = now.strftime('%Y-%m-%d %H:%M:%S')
        
        # Создаем DataFrame из данных пользователя
        df_new = pd.DataFrame([user_data])
        
        # Определяем порядок столбцов
        columns = ['datetime', 'category', 'name', 'city', 'phone', 'email']
        
        # Если файл существует, дополняем его
        if os.path.exists(EXCEL_FILE):
            df_existing = pd.read_excel(EXCEL_FILE)
            df_combined = pd.concat([df_existing, df_new], ignore_index=True)
            df_combined = df_combined[columns]  # Переупорядочиваем столбцы
            df_combined.to_excel(EXCEL_FILE, index=False)
        else:
            # Если файл не существует, создаем новый
            df_new = df_new[columns]  # Переупорядочиваем столбцы
            df_new.to_excel(EXCEL_FILE, index=False)
        
        logger.info(f"Данные пользователя сохранены: {user_data['name']}")
        return True
    
    except Exception as e:
        logger.error(f"Ошибка при сохранении данных: {e}")
        return False

def get_stats() -> int:
    """
    Возвращает количество записей в Excel-файле.
    
    Returns:
        int: Количество записей
    """
    try:
        if os.path.exists(EXCEL_FILE):
            df = pd.read_excel(EXCEL_FILE)
            return len(df)
        return 0
    except Exception as e:
        logger.error(f"Ошибка при получении статистики: {e}")
        return -1