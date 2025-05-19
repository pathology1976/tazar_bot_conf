from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# Клавиатура для выбора категории
def get_category_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.add(
        KeyboardButton(text="Частное лицо"),
        KeyboardButton(text="Заводчик"),
        KeyboardButton(text="Питомник")
    )
    builder.adjust(3)  # Все три кнопки в одном ряду
    return builder.as_markup(resize_keyboard=True)

# Клавиатура для навигации по форме
def get_form_keyboard(include_back=True) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    
    if include_back:
        builder.add(KeyboardButton(text="Назад"))
    
    builder.add(KeyboardButton(text="Отмена"))
    builder.adjust(2)  # По две кнопки в ряд
    return builder.as_markup(resize_keyboard=True)

# Клавиатура для подтверждения введенных данных
def get_confirm_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.add(
        KeyboardButton(text="Подтвердить"),
        KeyboardButton(text="Изменить"),
        KeyboardButton(text="Отмена")
    )
    builder.adjust(2)  # По две кнопки в ряд
    return builder.as_markup(resize_keyboard=True)