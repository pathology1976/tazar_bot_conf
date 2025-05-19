from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from states import RegistrationForm
from keyboards import get_category_keyboard, get_form_keyboard, get_confirm_keyboard
from validators import validate_phone, validate_email
from utils import save_user_data, get_stats
from config import ADMIN_IDS, EXCEL_FILE, logger

router = Router()

# Обработчик команды /start
@router.message(Command("start"), StateFilter(default_state))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Добро пожаловать в Tazar-бота! Этот бот поможет нам познакомиться ближе, и не потеряться. Пожалуйста, выберите свою категорию:",
        reply_markup=get_category_keyboard()
    )
    await state.set_state(RegistrationForm.category)

# Обработчик выбора категории
@router.message(StateFilter(RegistrationForm.category))
async def process_category(message: Message, state: FSMContext):
    categories = ["Частное лицо", "Заводчик", "Питомник"]
    
    if message.text not in categories:
        await message.answer(
            "Пожалуйста, выберите категорию, используя клавиатуру ниже:",
            reply_markup=get_category_keyboard()
        )
        return
    
    await state.update_data(category=message.text)
    await message.answer(
        "Теперь введите ваши Имя и Фамилию:",
        reply_markup=get_form_keyboard(include_back=False)
    )
    await state.set_state(RegistrationForm.name)

# Обработчик ввода ФИО
@router.message(StateFilter(RegistrationForm.name))
async def process_name(message: Message, state: FSMContext):
    if message.text == "Отмена":
        await cancel_handler(message, state)
        return
    
    await state.update_data(name=message.text)
    await message.answer(
        "Движемся дальше. Теперь укажите ваш город:",
        reply_markup=get_form_keyboard()
    )
    await state.set_state(RegistrationForm.city)

# Обработчик ввода города
@router.message(StateFilter(RegistrationForm.city))
async def process_city(message: Message, state: FSMContext):
    if message.text == "Отмена":
        await cancel_handler(message, state)
        return
    
    if message.text == "Назад":
        await message.answer(
            "Введите ваше ФИО:",
            reply_markup=get_form_keyboard(include_back=False)
        )
        await state.set_state(RegistrationForm.name)
        return
    
    await state.update_data(city=message.text)
    await message.answer(
        "Осталось совсем немного. Укажите ваш номер телефона:",
        reply_markup=get_form_keyboard()
    )
    await state.set_state(RegistrationForm.phone)

# Обработчик ввода телефона
@router.message(StateFilter(RegistrationForm.phone))
async def process_phone(message: Message, state: FSMContext):
    if message.text == "Отмена":
        await cancel_handler(message, state)
        return
    
    if message.text == "Назад":
        await message.answer(
            "Введите ваш город:",
            reply_markup=get_form_keyboard()
        )
        await state.set_state(RegistrationForm.city)
        return
    
    # Валидация телефона
    if not validate_phone(message.text):
        await message.answer(
            "Некорректный формат номера телефона. Пожалуйста, используйте только цифры, + и пробелы.",
            reply_markup=get_form_keyboard()
        )
        return
    
    await state.update_data(phone=message.text)
    await message.answer(
        f"Вы ввели: {message.text}\nВсё верно?",
        reply_markup=get_confirm_keyboard()
    )
    await state.set_state(RegistrationForm.confirm_phone)

# Обработчик подтверждения телефона
@router.message(StateFilter(RegistrationForm.confirm_phone))
async def process_confirm_phone(message: Message, state: FSMContext):
    if message.text == "Отмена":
        await cancel_handler(message, state)
        return
    
    if message.text == "Изменить":
        await message.answer(
            "Введите ваш номер телефона (только цифры, + и пробелы):",
            reply_markup=get_form_keyboard()
        )
        await state.set_state(RegistrationForm.phone)
        return
    
    if message.text == "Подтвердить":
        await message.answer(
            "Введите ваш email:",
            reply_markup=get_form_keyboard()
        )
        await state.set_state(RegistrationForm.email)
        return
    
    await message.answer(
        "Пожалуйста, используйте кнопки для ответа.",
        reply_markup=get_confirm_keyboard()
    )

# Обработчик ввода email
@router.message(StateFilter(RegistrationForm.email))
async def process_email(message: Message, state: FSMContext):
    if message.text == "Отмена":
        await cancel_handler(message, state)
        return
    
    if message.text == "Назад":
        await message.answer(
            "Введите ваш номер телефона (только цифры, + и пробелы):",
            reply_markup=get_form_keyboard()
        )
        await state.set_state(RegistrationForm.phone)
        return
    
    # Валидация email
    if not validate_email(message.text):
        await message.answer(
            "Некорректный формат email. Пожалуйста, введите email в формате example@domain.com",
            reply_markup=get_form_keyboard()
        )
        return
    
    await state.update_data(email=message.text)
    
    # Получаем все данные
    user_data = await state.get_data()
    
    # Сохраняем данные в Excel
    if save_user_data(user_data):
        await message.answer(
            "Вот и все! Большое спасибо! Ваши данные успешно сохранены. Теперь мы точно не потеряемся.",
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        await message.answer(
            "Произошла ошибка при сохранении данных. Пожалуйста, попробуйте позже.",
            reply_markup=ReplyKeyboardRemove()
        )
    
    # Очищаем состояние
    await state.clear()
    return
    
    await message.answer(
        "Пожалуйста, используйте кнопки для ответа.",
        reply_markup=get_confirm_keyboard()
    )

# Обработчик отмены на любом этапе
async def cancel_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    
    logger.info(f"Отмена операции пользователем {message.from_user.id}")
    await state.clear()
    await message.answer(
        "Операция отменена. Все введенные данные удалены.",
        reply_markup=ReplyKeyboardRemove()
    )

# Обработчик команды /export (только для админов)
@router.message(Command("export"))
async def cmd_export(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("У вас нет доступа к этой команде.")
        return
    
    try:
        if not EXCEL_FILE.exists():
            await message.answer("Файл с данными еще не создан.")
            return
        
        # Используем FSInputFile вместо прямого пути к файлу
        from aiogram.types import FSInputFile
        file = FSInputFile(EXCEL_FILE)
        
        await message.answer_document(
            document=file,
            caption="Текущий файл с данными пользователей."
        )
        logger.info(f"Файл экспортирован администратором {message.from_user.id}")
    except Exception as e:
        logger.error(f"Ошибка при экспорте файла: {e}")
        await message.answer(f"Произошла ошибка при экспорте файла: {e}")

# Обработчик команды /stats (только для админов)
@router.message(Command("stats"))
async def cmd_stats(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("У вас нет доступа к этой команде.")
        return
    
    count = get_stats()
    if count >= 0:
        await message.answer(f"Количество собранных анкет: {count}")
    else:
        await message.answer("Произошла ошибка при получении статистики.")