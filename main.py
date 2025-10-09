import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters.command import Command
from aiogram import F

from config import API_TOKEN, init_db, recreate_db
from handlers import (
    cmd_start, cmd_quiz, show_stats, reset_progress, 
    right_answer, wrong_answer, next_question_handler, finish_quiz_handler
)

# Объект бота
bot = Bot(token=API_TOKEN)
# Диспетчер
dp = Dispatcher()

# Регистрация обработчиков
dp.message.register(cmd_start, Command("start"))
dp.message.register(cmd_quiz, Command("quiz"))
dp.message.register(cmd_quiz, F.text == "Начать игру")
dp.message.register(show_stats, F.text == "Моя статистика")
dp.message.register(reset_progress, F.text == "Сбросить прогресс")
dp.message.register(next_question_handler, F.text == "Следующий вопрос")
dp.message.register(finish_quiz_handler, F.text == "Завершить квиз")

dp.callback_query.register(right_answer, F.data == "right_answer")
dp.callback_query.register(wrong_answer, F.data == "wrong_answer")

async def main():
    # Пересоздаем базу данных для исправления структуры
    await recreate_db()
    print("База данных пересоздана с новой структурой")
    
    # Запуск бота
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())