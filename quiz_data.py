# Структура квиза с 10 вопросами о программировании и Python
# Структура квиза с 10 вопросами о программировании и Python
quiz_data = [
    {
        'question': 'Что такое Python?',
        'options': [
            'Язык программирования',
            'Тип данных', 
            'Музыкальный инструмент',
            'Змея на английском'
        ],
        'correct_option': 0,
        'explanation': 'Python - это высокоуровневый язык программирования общего назначения.'
    },
    {
        'question': 'Какой тип данных используется для хранения целых чисел?',
        'options': [
            'int',
            'float', 
            'str',
            'natural'
        ],
        'correct_option': 0,
        'explanation': 'int (integer) используется для хранения целых чисел.'
    },
    {
        'question': 'Какой оператор используется для возведения в степень в Python?',
        'options': [
            '**',
            '^',
            'pow',
            '//'
        ],
        'correct_option': 0,
        'explanation': 'Оператор ** используется для возведения в степень, например: 2**3 = 8.'
    },
    {
        'question': 'Что выведет этот код: print("Hello" + "World")?',
        'options': [
            'HelloWorld',
            'Hello World',
            'Hello+World', 
            'Ошибку'
        ],
        'correct_option': 0,
        'explanation': 'Оператор + конкатенирует строки без пробела между ними.'
    },
    {
        'question': 'Какой из этих типов данных является изменяемым (mutable) в Python?',
        'options': [
            'list',
            'tuple',
            'str',
            'int'
        ],
        'correct_option': 0,
        'explanation': 'List (список) является изменяемым, а tuple, str и int - неизменяемыми.'
    },
    {
        'question': 'Что делает метод append() у списков?',
        'options': [
            'Добавляет элемент в конец списка',
            'Удаляет последний элемент',
            'Сортирует список',
            'Объединяет два списка'
        ],
        'correct_option': 0,
        'explanation': 'Метод append() добавляет переданный элемент в конец списка.'
    },
    {
        'question': 'Какой символ используется для однострочных комментариев в Python?',
        'options': [
            '#',
            '//',
            '--',
            '/*'
        ],
        'correct_option': 0,
        'explanation': 'Символ # используется для однострочных комментариев в Python.'
    },
    {
        'question': 'Что вернет выражение: 7 // 2?',
        'options': [
            '3',
            '3.5',
            '4',
            '1'
        ],
        'correct_option': 0,
        'explanation': 'Оператор // выполняет целочисленное деление, отбрасывая дробную часть.'
    },
    {
        'question': 'Какой метод используется для получения длины списка?',
        'options': [
            'len()',
            'length()',
            'size()',
            'count()'
        ],
        'correct_option': 0,
        'explanation': 'Функция len() возвращает количество элементов в списке.'
    },
    {
        'question': 'Что такое PEP 8?',
        'options': [
            'Руководство по стилю кода Python',
            'Новая версия Python',
            'Библиотека для работы с данными',
            'Система управления пакетами'
        ],
        'correct_option': 0,
        'explanation': 'PEP 8 - это руководство по написанию читаемого кода на Python.'
    }
]

def get_quiz_data():
    return quiz_data

def get_question_by_index(index):
    if 0 <= index < len(quiz_data):
        return quiz_data[index]
    return None

def get_total_questions():
    return len(quiz_data)