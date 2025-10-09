import logging
import aiosqlite
import os

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Токен бота
API_TOKEN = '8458819912:AAEc7Z3Vrxr-d5z-KO9l3FhOtCgowCR3x-Y'

# Настройки базы данных
DB_NAME = 'quiz_bot.db'

async def init_db():
    """Инициализация базы данных"""
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS quiz_state (
                user_id INTEGER PRIMARY KEY,
                question_index INTEGER DEFAULT 0,
                score INTEGER DEFAULT 0
            )
        ''')
        await db.commit()

async def get_quiz_index(user_id):
    """Получить текущий индекс вопроса для пользователя"""
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT question_index FROM quiz_state WHERE user_id = ?', (user_id,)) as cursor:
            results = await cursor.fetchone()
            if results is not None:
                return results[0]
            else:
                return 0

async def get_user_score(user_id):
    """Получить счет пользователя"""
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT score FROM quiz_state WHERE user_id = ?', (user_id,)) as cursor:
            results = await cursor.fetchone()
            if results is not None:
                return results[0]
            else:
                return 0

async def update_quiz_index(user_id, index):
    """Обновить индекс вопроса для пользователя"""
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            'INSERT OR REPLACE INTO quiz_state (user_id, question_index, score) VALUES (?, ?, COALESCE((SELECT score FROM quiz_state WHERE user_id = ?), 0))',
            (user_id, index, user_id)
        )
        await db.commit()

async def update_user_score(user_id, score):
    """Обновить счет пользователя"""
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            'INSERT OR REPLACE INTO quiz_state (user_id, question_index, score) VALUES (?, COALESCE((SELECT question_index FROM quiz_state WHERE user_id = ?), 0), ?)',
            (user_id, user_id, score)
        )
        await db.commit()

async def reset_user_progress(user_id):
    """Сбросить прогресс пользователя"""
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            'INSERT OR REPLACE INTO quiz_state (user_id, question_index, score) VALUES (?, 0, 0)',
            (user_id,)
        )
        await db.commit()

async def recreate_db():
    """Пересоздать базу данных (для исправления структуры)"""
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
    await init_db()