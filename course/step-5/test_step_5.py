import pytest
import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from typing import List, Dict
from functions_step_5 import qdrant_client, upload_faq_to_qdrant, upload_info_to_qdrant


# Вспомогательная функция для создания случайных эмбеддингов
def generate_random_embeddings(num_embeddings: int, dim: int):
    return np.random.rand(num_embeddings, dim)
    

##### ПРОВЕРКА РАБОТЫ ВЕКТОРНОЙ БД ПРИ РАБОТЕ С FAQ #####

# Тест 1: Проверка успешной загрузки данных в коллекцию Qdrant
def test_upload_faq_to_qdrant():
    chunks = [
        {'chunk_id': '1', 'course_name': 'Курс 1', 'course_url': 'url1', 'question_and_answer': 'Вопрос: Как зарегистрироваться? Ответ: Перейдите по ссылке', 'metadata': {}},
        {'chunk_id': '2', 'course_name': 'Курс 1', 'course_url': 'url1', 'question_and_answer': 'Вопрос: Как отменить подписку? Ответ: Напишите в поддержку', 'metadata': {}}
    ]
    embeddings = generate_random_embeddings(len(chunks), 512)  # Предположим, что размер эмбеддингов — 512

    # Загружаем данные в коллекцию
    upload_faq_to_qdrant(chunks, embeddings, collection_name="test_faq_collection", сourse_vector_length=512)
    
    # Проверяем, что коллекция была создана
    assert qdrant_client.collection_exists("test_faq_collection"), "Ошибка: коллекция не была создана в Qdrant"

    # Очищаем коллекцию после теста
    qdrant_client.delete_collection("test_faq_collection")


# Тест 2: Проверка удаления коллекции, если она существует
def test_faq_collection_deletion_if_exists():
    chunks = [
        {'chunk_id': '1', 'course_name': 'Курс 1', 'course_url': 'url1', 'question_and_answer': 'Вопрос: Что такое курс? Ответ: Это обучение', 'metadata': {}}
    ]
    embeddings = generate_random_embeddings(len(chunks), 512)

    # Создаем коллекцию в первый раз
    upload_faq_to_qdrant(chunks, embeddings, collection_name="test_faq_collection", сourse_vector_length=512)
    
    # Проверяем, что коллекция существует
    assert qdrant_client.collection_exists("test_faq_collection"), "Ошибка: коллекция не была создана в Qdrant"

    # Загружаем данные в коллекцию снова (должна быть удалена и заново создана)
    upload_faq_to_qdrant(chunks, embeddings, collection_name="test_faq_collection", сourse_vector_length=512)

    # Проверяем, что коллекция существует после удаления и повторного создания
    assert qdrant_client.collection_exists("test_faq_collection"), "Ошибка: коллекция не была повторно создана в Qdrant"

    # Очищаем коллекцию после теста
    qdrant_client.delete_collection("test_faq_collection")


# Тест 3: Проверка, что эмбеддинги соответствуют ожидаемому размеру
def test_faq_embeddings_size():
    chunks = [
        {'chunk_id': '1', 'course_name': 'Курс 1', 'course_url': 'url1', 'question_and_answer': 'Вопрос: Как начать курс? Ответ: Начните с урока 1', 'metadata': {}}
    ]
    embeddings = generate_random_embeddings(len(chunks), 512)  # 512 — размер эмбеддинга

    # Загружаем данные в коллекцию
    upload_faq_to_qdrant(chunks, embeddings, collection_name="test_faq_collection", сourse_vector_length=512)

    # Проверяем размер эмбеддингов
    assert embeddings.shape[1] == 512, "Ошибка: размер эмбеддингов не соответствует ожидаемому"

    # Очищаем коллекцию после теста
    qdrant_client.delete_collection("test_faq_collection")


# Тест 4: Проверка пустых данных (если коллекция пустая, она не должна загружаться)
def test_faq_empty_data():
    chunks = []  # Пустые данные
    embeddings = np.array([])  # Пустые эмбеддинги

    # Загружаем пустые данные
    upload_faq_to_qdrant(chunks, embeddings, collection_name="test_faq_collection", сourse_vector_length=512)

    # Проверяем, что коллекция не была создана
    assert not qdrant_client.collection_exists("test_faq_collection"), "Ошибка: коллекция не должна была быть создана с пустыми данными"


# Тест 5: Проверка, что функция корректно удаляет коллекцию после загрузки данных
def test_faq_collection_deletion_after_upload():
    chunks = [
        {'chunk_id': '1', 'course_name': 'Курс 1', 'course_url': 'url1', 'question_and_answer': 'Вопрос: Как получить доступ? Ответ: Зарегистрируйтесь', 'metadata': {}}
    ]
    embeddings = generate_random_embeddings(len(chunks), 512)

    # Загружаем данные в коллекцию
    upload_faq_to_qdrant(chunks, embeddings, collection_name="test_faq_collection", сourse_vector_length=512)
    
    # Проверяем, что коллекция существует после загрузки
    assert qdrant_client.collection_exists("test_faq_collection"), "Ошибка: коллекция не была создана в Qdrant"
    
    # Очищаем коллекцию после теста
    qdrant_client.delete_collection("test_faq_collection")
    
    # Проверяем, что коллекция была удалена
    assert not qdrant_client.collection_exists("test_faq_collection"), "Ошибка: коллекция не была удалена после теста"
    
    
##### ПРАВИЛЬНОСТЬ РАБОТЫ ВЕКТОРНОЙ БАЗЫ ДАННЫХ ПРИ РАБОТЕ С ОПИСАНИЕМ КУРСОВ

# Тест 1: Проверка успешной загрузки данных в коллекцию Qdrant
def test_upload_info_to_qdrant():
    chunks = [
        {'chunk_id': '1', 'course_name': 'Курс 1', 'course_url': 'url1', 'sequence': 'Описание 1', 'categories': ['Категория 1'], 'metadata': {}},
        {'chunk_id': '2', 'course_name': 'Курс 2', 'course_url': 'url2', 'sequence': 'Описание 2', 'categories': ['Категория 2'], 'metadata': {}}
    ]
    embeddings = generate_random_embeddings(len(chunks), 512)  # Предположим, что размер эмбеддингов — 512

    # Загружаем данные в коллекцию
    upload_info_to_qdrant(chunks, embeddings, collection_name="test_info_collection")
    
    # Проверяем, что коллекция была создана
    assert qdrant_client.collection_exists("test_info_collection"), "Ошибка: коллекция не была создана в Qdrant"

    # Очищаем коллекцию после теста
    qdrant_client.delete_collection("test_info_collection")


# Тест 2: Проверка удаления коллекции, если она существует
def test_info_collection_deletion_if_exists():
    chunks = [
        {'chunk_id': '1', 'course_name': 'Курс 1', 'course_url': 'url1', 'sequence': 'Описание 1', 'categories': ['Категория 1'], 'metadata': {}}
    ]
    embeddings = generate_random_embeddings(len(chunks), 512)

    # Создаем коллекцию в первый раз
    upload_info_to_qdrant(chunks, embeddings, collection_name="test_info_collection")
    
    # Проверяем, что коллекция существует
    assert qdrant_client.collection_exists("test_info_collection"), "Ошибка: коллекция не была создана в Qdrant"

    # Загружаем данные в коллекцию снова (должна быть удалена и заново создана)
    upload_info_to_qdrant(chunks, embeddings, collection_name="test_info_collection")

    # Проверяем, что коллекция существует после удаления и повторного создания
    assert qdrant_client.collection_exists("test_info_collection"), "Ошибка: коллекция не была повторно создана в Qdrant"

    # Очищаем коллекцию после теста
    qdrant_client.delete_collection("test_info_collection")


# Тест 3: Проверка, что эмбеддинги соответствуют ожидаемому размеру
def test_info_embeddings_size():
    chunks = [
        {'chunk_id': '1', 'course_name': 'Курс 1', 'course_url': 'url1', 'sequence': 'Описание 1', 'categories': ['Категория 1'], 'metadata': {}}
    ]
    embeddings = generate_random_embeddings(len(chunks), 512)  # 512 — размер эмбеддинга

    # Загружаем данные в коллекцию
    upload_info_to_qdrant(chunks, embeddings, collection_name="test_info_collection")

    # Проверяем размер эмбеддингов
    assert embeddings.shape[1] == 512, "Ошибка: размер эмбеддингов не соответствует ожидаемому"

    # Очищаем коллекцию после теста
    qdrant_client.delete_collection("test_info_collection")


# Тест 4: Проверка пустых данных (если коллекция пустая, она не должна загружаться)
def test_info_empty_data():
    chunks = []  # Пустые данные
    embeddings = np.array([])  # Пустые эмбеддинги

    # Загружаем пустые данные
    upload_info_to_qdrant(chunks, embeddings, collection_name="test_info_collection")

    # Проверяем, что коллекция не была создана
    assert not qdrant_client.collection_exists("test_info_collection"), "Ошибка: коллекция не должна была быть создана с пустыми данными"


# Тест 5: Проверка, что функция корректно удаляет коллекцию после загрузки данных
def test_info_collection_deletion_after_upload():
    chunks = [
        {'chunk_id': '1', 'course_name': 'Курс 1', 'course_url': 'url1', 'sequence': 'Описание 1', 'categories': ['Категория 1'], 'metadata': {}}
    ]
    embeddings = generate_random_embeddings(len(chunks), 512)

    # Загружаем данные в коллекцию
    upload_info_to_qdrant(chunks, embeddings, collection_name="test_info_collection")
    
    # Проверяем, что коллекция существует после загрузки
    assert qdrant_client.collection_exists("test_info_collection"), "Ошибка: коллекция не была создана в Qdrant"
    
    # Очищаем коллекцию после теста
    qdrant_client.delete_collection("test_info_collection")
    
    # Проверяем, что коллекция была удалена
    assert not qdrant_client.collection_exists("test_info_collection"), "Ошибка: коллекция не была удалена после теста"
