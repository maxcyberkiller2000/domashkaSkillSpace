from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram import types
from quiz_data import get_question_by_index

def generate_options_keyboard(current_question_index):
    """Генерация клавиатуры с вариантами ответов"""
    question_data = get_question_by_index(current_question_index)
    if not question_data:
        return None
        
    builder = InlineKeyboardBuilder()
    answer_options = question_data['options']
    correct_option = question_data['correct_option']
    
    for i, option in enumerate(answer_options):
        builder.add(types.InlineKeyboardButton(
            text=option,
            callback_data="right_answer" if i == correct_option else "wrong_answer")
        )
    
    builder.adjust(1)
    return builder.as_markup()

def get_main_keyboard():
    """Главная клавиатура"""
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Начать игру"))
    builder.add(types.KeyboardButton(text="Моя статистика"))
    builder.add(types.KeyboardButton(text="Сбросить прогресс"))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

def get_quiz_control_keyboard():
    """Клавиатура для управления квизом"""
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Следующий вопрос"))
    builder.add(types.KeyboardButton(text="Завершить квиз"))
    builder.add(types.KeyboardButton(text="Моя статистика"))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)