import pytest
import pandas as pd
from typing import Dict, List
from functions_step_4 import prepare_faq_chunks, prepare_info_chunks

##### ПРОВЕРКА ПРАВИЛЬНОСТИ ЧАНКОВ С ВОПРОСАМИ И ОТВЕТАМИ #####

# Тест 1: Проверка корректности обработки FAQ и DataFrame
def test_prepare_faq_chunks_basic():
    faq_collection = {
        'url1': [
            'Вопрос: Как зарегистрироваться? Ответ: Перейдите по ссылке и следуйте инструкциям.',
            'Вопрос: Как отменить подписку? Ответ: Напишите в поддержку.'
        ],
        'url2': [
            'Вопрос: Как начать курс? Ответ: Зарегистрируйтесь и начните обучение.'
        ]
    }
    
    courses_df = pd.DataFrame({
        'course_url': ['url1', 'url2'],
        'course_name': ['Курс 1', 'Курс 2']
    })
    
    expected_result = [
        {
            'chunk_id': 'url1_0',
            'course_name': 'Курс 1',
            'course_url': 'url1',
            'question_and_answer': 'Вопрос: Как зарегистрироваться? Ответ: Перейдите по ссылке и следуйте инструкциям.',
            'metadata': {
                'chunk_type': 'qa',
                'course_id': 'url1',
                'qa_index': 0,
                'total_qa_pairs': 2
            }
        },
        {
            'chunk_id': 'url1_1',
            'course_name': 'Курс 1',
            'course_url': 'url1',
            'question_and_answer': 'Вопрос: Как отменить подписку? Ответ: Напишите в поддержку.',
            'metadata': {
                'chunk_type': 'qa',
                'course_id': 'url1',
                'qa_index': 1,
                'total_qa_pairs': 2
            }
        },
        {
            'chunk_id': 'url2_0',
            'course_name': 'Курс 2',
            'course_url': 'url2',
            'question_and_answer': 'Вопрос: Как начать курс? Ответ: Зарегистрируйтесь и начните обучение.',
            'metadata': {
                'chunk_type': 'qa',
                'course_id': 'url2',
                'qa_index': 0,
                'total_qa_pairs': 1
            }
        }
    ]
    
    result = prepare_faq_chunks(faq_collection, courses_df)
    
    assert result == expected_result, "Ошибка: неверный формат или данные выходного списка чанков"
    
# Тест 2: Проверка корректности формирования chunk_id
def test_prepare_faq_chunks_chunk_id():
    faq_collection = {
        'url1': [
            {'question_and_answer': [
            'Вопрос: Как получить доступ? Ответ: Регистрация на платформе.',
            'Вопрос: Как начать курс? Ответ: Начните с первого урока.'
        ], 
        'categories': ['Категория 1']}
        ]
    }
    
    courses_df = pd.DataFrame({
        'course_url': ['url1'],
        'course_name': ['Курс 1']
    })
    
    result = prepare_faq_chunks(faq_collection, courses_df)
    
    # Проверяем, что id чанков начинается с правильного значения
    assert result[0]['chunk_id'] == 'url1_0', "Ошибка: неверный формат chunk_id"

# Тест 3: Проверка правильности формирования метаданных
def test_prepare_faq_chunks_metadata():
    faq_collection = {
        'url1': ['Вопрос: Как получить доступ? Ответ: Регистрация на платформе.']
    }
    
    courses_df = pd.DataFrame({
        'course_url': ['url1'],
        'course_name': ['Курс 1']
    })
    
    result = prepare_faq_chunks(faq_collection, courses_df)
    
    chunk = result[0]

    assert chunk['metadata']['chunk_type'] == 'qa', "Ошибка: некорректный тип чанка в метаданных"
    assert chunk['metadata']['course_id'] == 'url1', "Ошибка: неправильный course_id в метаданных"
    assert chunk['metadata']['qa_index'] == 0, "Ошибка: индекс вопроса-ответа в метаданных не совпадает с ожидаемым"
    assert chunk['metadata']['total_qa_pairs'] == 1, "Ошибка: общее количество пар QA неверное"

# Тест 4: Проверка работы с параметром start_id
def test_prepare_faq_chunks_start_id():
    faq_collection = {
        'url1': [
            'Вопрос: Как получить доступ? Ответ: Регистрация на платформе.',
            'Вопрос: Как начать курс? Ответ: Начните с первого урока.'
        ]
    }
    
    courses_df = pd.DataFrame({
        'course_url': ['url1'],
        'course_name': ['Курс 1']
    })
    
    # Задаем start_id = 10
    result = prepare_faq_chunks(faq_collection, courses_df, start_id=10)
    
    assert result[0]['chunk_id'] == 'url1_10', "Ошибка: первый chunk_id не совпадает с ожидаемым"
    assert result[1]['chunk_id'] == 'url1_11', "Ошибка: второй chunk_id не совпадает с ожидаемым"

# Тест 5: Проверка работы с пустыми данными
def test_prepare_faq_chunks_empty():
    faq_collection = {}
    courses_df = pd.DataFrame(columns=['course_url', 'course_name'])
    
    result = prepare_faq_chunks(faq_collection, courses_df)
    
    assert result == [], "Ошибка: функция должна возвращать пустой список при отсутствии данных"
    
    
##### ПРОВЕРКА ПРАВИЛЬНОСТИ ЧАНКОВ С ИНФОРМАЦИЕЙ О КУРСАХ #####

# Тест 1: Проверка корректности подготовки чанков с описаниями и категориями
def test_prepare_info_chunks_basic():
    info_collection = {
        'url1': [
            {'sequence': 'Описание курса 1', 'categories': ['Категория 1', 'Категория 2']},
            {'sequence': 'Описание курса 2', 'categories': ['Категория 1']}
        ],
        'url2': [
            {'sequence': 'Описание курса 3', 'categories': ['Категория 3']}
        ]
    }
    
    courses_df = pd.DataFrame({
        'course_url': ['url1', 'url2'],
        'course_name': ['Курс 1', 'Курс 2']
    })
    
    expected_result = [
        {
            'chunk_id': 'url1_0',
            'course_name': 'Курс 1',
            'course_url': 'url1',
            'sequence': 'Описание курса 1',
            'categories': ['Категория 1', 'Категория 2'],
            'metadata': {
                'chunk_type': 'course_information',
                'course_id': 'url1',
                'course_information_index': 0,
                'total_sequences': 2
            }
        },
        {
            'chunk_id': 'url1_1',
            'course_name': 'Курс 1',
            'course_url': 'url1',
            'sequence': 'Описание курса 2',
            'categories': ['Категория 1'],
            'metadata': {
                'chunk_type': 'course_information',
                'course_id': 'url1',
                'course_information_index': 1,
                'total_sequences': 2
            }
        },
        {
            'chunk_id': 'url2_0',
            'course_name': 'Курс 2',
            'course_url': 'url2',
            'sequence': 'Описание курса 3',
            'categories': ['Категория 3'],
            'metadata': {
                'chunk_type': 'course_information',
                'course_id': 'url2',
                'course_information_index': 0,
                'total_sequences': 1
            }
        }
    ]
    
    result = prepare_info_chunks(info_collection, courses_df)
    
    assert result == expected_result, "Ошибка: данные чанков не соответствуют ожидаемому формату"

# Тест 2: Проверка корректности формирования chunk_id
def test_prepare_info_chunks_chunk_id():
    info_collection = {
        'url1': [
            {'sequence': 'Описание курса 1', 'categories': ['Категория 1']}
        ]
    }
    
    courses_df = pd.DataFrame({
        'course_url': ['url1'],
        'course_name': ['Курс 1']
    })
    
    result = prepare_info_chunks(info_collection, courses_df)
    
    # Проверяем, что id чанков начинается с правильного значения
    assert result[0]['chunk_id'] == 'url1_0', "Ошибка: неверный формат chunk_id"

# Тест 3: Проверка работы с параметром start_id
def test_prepare_info_chunks_start_id():
    info_collection = {
        'url1': [
            {'sequence': 'Описание курса 1', 'categories': ['Категория 1']},
            {'sequence': 'Описание курса 2', 'categories': ['Категория 2']}
        ]
    }
    
    courses_df = pd.DataFrame({
        'course_url': ['url1'],
        'course_name': ['Курс 1']
    })
    
    # Задаем start_id = 5
    result = prepare_info_chunks(info_collection, courses_df, start_id=5)
    
    # Проверяем, что id чанков начинаются с 5
    assert result[0]['chunk_id'] == 'url1_5', "Ошибка: первый chunk_id не совпадает с ожидаемым"
    assert result[1]['chunk_id'] == 'url1_6', "Ошибка: второй chunk_id не совпадает с ожидаемым"

# Тест 4: Проверка корректности формирования метаданных
def test_prepare_info_chunks_metadata():
    info_collection = {
        'url1': [{'sequence': 'Описание курса 1', 'categories': ['Категория 1']}]
    }
    
    courses_df = pd.DataFrame({
        'course_url': ['url1'],
        'course_name': ['Курс 1']
    })
    
    result = prepare_info_chunks(info_collection, courses_df)
    
    chunk = result[0]
    
    assert chunk['metadata']['chunk_type'] == 'course_information', "Ошибка: некорректный тип чанка в метаданных"
    assert chunk['metadata']['course_id'] == 'url1', "Ошибка: неверный course_id в метаданных"
    assert chunk['metadata']['course_information_index'] == 0, "Ошибка: неверный индекс курса в метаданных"
    assert chunk['metadata']['total_sequences'] == 1, "Ошибка: неверное количество последовательностей в метаданных"

# Тест 5: Проверка работы с пустыми данными
def test_prepare_info_chunks_empty():
    info_collection = {}
    courses_df = pd.DataFrame(columns=['course_url', 'course_name'])
    
    result = prepare_info_chunks(info_collection, courses_df)
    
    assert result == [], "Ошибка: функция должна возвращать пустой список при отсутствии данных"
