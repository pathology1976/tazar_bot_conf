from aiogram.fsm.state import State, StatesGroup

class RegistrationForm(StatesGroup):
    """Состояния для формы регистрации"""
    category = State()  # Выбор категории
    name = State()      # ФИО
    city = State()      # Город
    phone = State()     # Телефон
    email = State()     # Email
    confirm_name = State()    # Подтверждение ФИО
    confirm_city = State()    # Подтверждение города
    confirm_phone = State()   # Подтверждение телефона
    confirm_email = State()   # Подтверждение email