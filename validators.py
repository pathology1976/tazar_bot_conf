import re

def validate_phone(phone: str) -> bool:
    """
    Валидация номера телефона.
    Допускаются только цифры, + и пробелы.
    """
    # Удаляем пробелы для проверки
    cleaned_phone = phone.replace(' ', '')
    
    # Проверяем, что строка начинается с + (опционально) и содержит только цифры
    pattern = r'^\+?\d+$'
    
    return bool(re.match(pattern, cleaned_phone))

def validate_email(email: str) -> bool:
    """
    Валидация email.
    Проверяет формат email@domain
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    return bool(re.match(pattern, email))