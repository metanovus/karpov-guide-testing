from typing import List, Dict, Tuple
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from qdrant_client.models import PointStruct
from sentence_transformers import SentenceTransformer
import numpy as np


model = SentenceTransformer('DeepPavlov/rubert-base-cased-sentence')

qdrant_client = QdrantClient(
    url="https://e4a0270f-59cd-453d-9577-e33637c4ec29.us-east4-0.gcp.cloud.qdrant.io",
    api_key="gBVNUkVt2u7Mr-z5NcJnO4OX5gV2a6ztLW7nDvNrMupS5Mez1kNpZw"
)


def search_similar(query: str, top_k: int = 5) -> List[Tuple[str, object]]:
    """
    Ищет наиболее релевантные чанки в базе данных Qdrant, используя векторное представление запроса.

    Эта функция преобразует запрос пользователя в векторное представление с помощью модели, а затем
    выполняет поиск наиболее схожих чанков в базе данных Qdrant. Возвращает топ-N наиболее релевантных результатов.

    Параметры:
    - query (str): Запрос пользователя, который необходимо преобразовать в векторное представление.
    - top_k (int): Количество возвращаемых результатов. По умолчанию 5.

    Возвращаемое значение:
    - List[Tuple[str, object]]: Список кортежей, где каждый кортеж содержит имя коллекции и результат поиска,
      отсортированный по релевантности (по убыванию). Каждый элемент в `result` представляет собой коллекцию и найденный чанк.

    Пример:
    >>> result = search_similar("Какие курсы по Data Science вы предлагаете?")
    >>> print(result)  # [('karpov-guide-faq', <PointStruct>), ...]
    """
    query_embedding = model.encode(query, show_progress_bar=False)

    all_collections = qdrant_client.get_collections()
    result = []

    for collection in all_collections.collections:
        collection_name = collection.name
        
        search_result = qdrant_client.search(
            collection_name=collection_name,
            query_vector=query_embedding,
            limit=top_k
        )

        for seq in search_result:
            result.append((collection_name, seq))

    result = sorted(result, key=lambda x: x[1].score, reverse=True)
    
    return result
