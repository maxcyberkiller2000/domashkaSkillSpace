from aiogram import types, F
from aiogram.filters import Command
from config import get_quiz_index, update_quiz_index, get_user_score, update_user_score, reset_user_progress
from keyboards import generate_options_keyboard, get_main_keyboard, get_quiz_control_keyboard
from quiz_data import get_question_by_index, get_total_questions

# Хэндлер на команду /start
async def cmd_start(message: types.Message):
    await message.answer(
        "🎯 Добро пожаловать в квиз по Python!\n\n"
        "Проверьте свои знания программирования на Python. "
        "В квизе 10 вопросов разной сложности.",
        reply_markup=get_main_keyboard()
    )

async def get_question(message, user_id):
    """Показать вопрос пользователю"""
    current_question_index = await get_quiz_index(user_id)
    question_data = get_question_by_index(current_question_index)
    
    if question_data:
        kb = generate_options_keyboard(current_question_index)
        question_text = f"❓ Вопрос {current_question_index + 1}/{get_total_questions()}\n\n{question_data['question']}"
        await message.answer(question_text, reply_markup=kb)
    else:
        await message.answer("Ошибка: вопрос не найден")

async def new_quiz(message):
    """Начать новый квиз"""
    user_id = message.from_user.id
    await reset_user_progress(user_id)
    await message.answer("🚀 Начинаем новый квиз!", reply_markup=get_quiz_control_keyboard())
    await get_question(message, user_id)

# Хэндлер на команду /quiz
async def cmd_quiz(message: types.Message):
    await message.answer("🎮 Давайте начнем квиз!")
    await new_quiz(message)

# Показать статистику
async def show_stats(message: types.Message):
    user_id = message.from_user.id
    current_score = await get_user_score(user_id)
    current_question = await get_quiz_index(user_id)
    total_questions = get_total_questions()
    
    await message.answer(
        f"📊 Ваша статистика:\n\n"
        f"• Правильных ответов: {current_score}\n"
        f"• Текущий прогресс: {current_question}/{total_questions}\n"
        f"• Осталось вопросов: {total_questions - current_question}",
        reply_markup=get_main_keyboard()
    )

# Сброс прогресса
async def reset_progress(message: types.Message):
    user_id = message.from_user.id
    await reset_user_progress(user_id)
    await message.answer(
        "🔄 Ваш прогресс сброшен. Вы можете начать квиз заново!",
        reply_markup=get_main_keyboard()
    )

# Обработка правильного ответа
async def right_answer(callback: types.CallbackQuery):
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )

    user_id = callback.from_user.id
    current_question_index = await get_quiz_index(user_id)
    question_data = get_question_by_index(current_question_index)
    
    # Обновляем счет
    current_score = await get_user_score(user_id)
    await update_user_score(user_id, current_score + 1)
    
    await callback.message.answer(
        f"✅ Верно!\n\n💡 {question_data['explanation']}",
        reply_markup=get_quiz_control_keyboard()
    )
    
    # Переход к следующему вопросу
    await next_question(callback.message, user_id)

# Обработка неправильного ответа
async def wrong_answer(callback: types.CallbackQuery):
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )

    user_id = callback.from_user.id
    current_question_index = await get_quiz_index(user_id)
    question_data = get_question_by_index(current_question_index)
    
    correct_option = question_data['correct_option']
    correct_answer = question_data['options'][correct_option]

    await callback.message.answer(
        f"❌ Неправильно.\n\n"
        f"✅ Правильный ответ: {correct_answer}\n\n"
        f"💡 {question_data['explanation']}",
        reply_markup=get_quiz_control_keyboard()
    )
    
    # Переход к следующему вопросу
    await next_question(callback.message, user_id)

async def next_question(message, user_id):
    """Переход к следующему вопросу"""
    current_question_index = await get_quiz_index(user_id)
    current_question_index += 1
    await update_quiz_index(user_id, current_question_index)

    if current_question_index < get_total_questions():
        await get_question(message, user_id)
    else:
        # Квиз завершен
        final_score = await get_user_score(user_id)
        total_questions = get_total_questions()
        
        result_message = "🎉 Квиз завершен!\n\n"
        result_message += f"🏆 Ваш результат: {final_score}/{total_questions}\n\n"
        
        if final_score >= 8:
            result_message += "🔥 Отличный результат!"
        elif final_score >= 5:
            result_message += "👍 Хорошая работа!"
        else:
            result_message += "💪 Продолжайте практиковаться!"
            
        await message.answer(result_message, reply_markup=get_main_keyboard())

# Обработчик для кнопки "Следующий вопрос"
async def next_question_handler(message: types.Message):
    user_id = message.from_user.id
    current_question_index = await get_quiz_index(user_id)
    
    if current_question_index < get_total_questions():
        await get_question(message, user_id)
    else:
        await message.answer("Квиз уже завершен. Начните новый!", reply_markup=get_main_keyboard())

# Обработчик для кнопки "Завершить квиз"
async def finish_quiz_handler(message: types.Message):
    user_id = message.from_user.id
    final_score = await get_user_score(user_id)
    total_questions = get_total_questions()
    current_question = await get_quiz_index(user_id)
    
    await message.answer(
        f"📋 Квиз досрочно завершен!\n\n"
        f"• Пройдено вопросов: {current_question}/{total_questions}\n"
        f"• Правильных ответов: {final_score}\n\n"
        f"Можете начать заново в любое время!",
        reply_markup=get_main_keyboard()
    )