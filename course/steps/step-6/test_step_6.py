import pytest
import random
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from functions_step_6 import model, qdrant_client, search_similar


# Тест 1: Проверка существования коллекций 'karpov-guide-info' и 'karpov-guide-faq'
def test_collections_exist():
    collections = qdrant_client.get_collections().collections
    collection_names = [collection.name for collection in collections]
    
    assert 'karpov-guide-info' in collection_names, "Ошибка: коллекция 'karpov-guide-info' не найдена в базе данных"
    assert 'karpov-guide-faq' in collection_names, "Ошибка: коллекция 'karpov-guide-faq' не найдена в базе данных"


# Тест 2: Проверка работы с коллекциями 'karpov-guide-info' и 'karpov-guide-faq'
def test_search_similar():
    query = "Какие курсы по Data Science вы предлагаете?"
    
    # Ищем похожие объекты в обеих коллекциях
    result = search_similar(query, top_k=5)

    # Проверяем, что результат не пустой
    assert len(result) > 0, "Ошибка: не найдены похожие объекты"

    # Проверяем, что результат состоит из коллекции и объекта
    for collection_name, seq in result:
        assert collection_name in ['karpov-guide-info', 'karpov-guide-faq'], f"Ошибка: неверное имя коллекции {collection_name}"


# Тест 3: Проверка, что мы можем извлечь случайные объекты из обеих коллекций
def test_random_search():
    query = "Как начать курс?"
    
    # Выполняем поиск
    result = search_similar(query, top_k=5)
    
    # Проверяем, что мы получили хотя бы один результат для каждой коллекции
    collections = {'karpov-guide-info': False, 'karpov-guide-faq': False}
    
    for collection_name, seq in result:
        if collection_name in collections:
            collections[collection_name] = True
    
    assert collections['karpov-guide-info'], "Ошибка: не найдены результаты для коллекции 'karpov-guide-info'"
    assert collections['karpov-guide-faq'], "Ошибка: не найдены результаты для коллекции 'karpov-guide-faq'"


# Тест 4: Проверка корректности работы поиска с случайным запросом
def test_random_query_search():
    # Генерируем случайный запрос
    query = f"Тест {random.randint(1, 100)}"
    
    # Выполняем поиск
    result = search_similar(query, top_k=3)

    # Проверяем, что поиск вернул результат
    assert len(result) > 0, "Ошибка: поиск не вернул результатов для случайного запроса"
    
    # Проверяем, что результат состоит из кортежей с правильной структурой
    for collection_name, seq in result:
        assert collection_name in ['karpov-guide-info', 'karpov-guide-faq'], f"Ошибка: неверное имя коллекции {collection_name}"
