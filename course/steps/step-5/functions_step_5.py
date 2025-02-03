from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from qdrant_client.models import PointStruct
import numpy as np
from typing import List, Dict


qdrant_client = QdrantClient(
    url="https://e4a0270f-59cd-453d-9577-e33637c4ec29.us-east4-0.gcp.cloud.qdrant.io",
    api_key="gBVNUkVt2u7Mr-z5NcJnO4OX5gV2a6ztLW7nDvNrMupS5Mez1kNpZw"
)


def upload_faq_to_qdrant(chunks: List[Dict], embeddings: np.ndarray, collection_name: str = 'karpov-guide-faq', сourse_vector_length: int = 512):
    """
    Загружает данные в Qdrant с оптимизированными параметрами.

    Эта функция загружает чанки текста и их эмбеддинги в коллекцию Qdrant. 
    Если коллекция уже существует, она будет удалена и создана заново.

    Параметры:
    - chunks (List[Dict]): Список чанков, каждый из которых содержит текстовые данные (вопрос, ответ и метаданные).
    - embeddings (np.ndarray): Эмбеддинги для чанков, полученные после векторизации текста.
    - collection_name (str): Название коллекции в Qdrant. По умолчанию 'karpov-guide-faq'.

    Возвращаемое значение:
    - None
    """
    if any(chunks) and embeddings.any():
    
        if qdrant_client.collection_exists(collection_name):
            qdrant_client.delete_collection(collection_name)  # Удаляем, если уже создана
                
        qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=сourse_vector_length, distance=Distance.COSINE),
        )
        
        points = []
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            point = PointStruct(
                id=i,
                vector=embedding.tolist(),
                payload={
                    'chunk_id': chunk['chunk_id'],
                    'course_name': chunk['course_name'],
                    'course_url': chunk['course_url'],
                    'question_and_answer': chunk['question_and_answer'],
                    'metadata': chunk['metadata']
                }
            )
            points.append(point)
        
        qdrant_client.upload_points(
            collection_name=collection_name,
            points=points,
            batch_size=30
        )
        
        
def upload_info_to_qdrant(chunks: List[Dict], embeddings: np.ndarray, collection_name: str = 'karpov-guide-info', сourse_vector_length: int = 768):
    """
    Загружает данные в Qdrant с оптимизированными параметрами.

    Эта функция загружает чанки основной информации о курсах и их эмбеддинги в коллекцию Qdrant. 
    Если коллекция уже существует, она будет удалена и создана заново.

    Параметры:
    - chunks (List[Dict]): Список чанков с основной информацией о курсе, включая описание и категории.
    - embeddings (np.ndarray): Эмбеддинги для чанков, полученные после векторизации текста.
    - collection_name (str): Название коллекции в Qdrant. По умолчанию 'karpov-guide-info'.

    Возвращаемое значение:
    - None
    """
    if any(chunks) and embeddings.any():
        if qdrant_client.collection_exists(collection_name):
            qdrant_client.delete_collection(collection_name)  # Удаляем, если уже создана
                
        qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=сourse_vector_length, distance=Distance.COSINE),
        )
        
        points = []
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            point = PointStruct(
                id=i,
                vector=embedding.tolist(),
                payload={
                    'chunk_id': chunk['chunk_id'],
                    'course_name': chunk['course_name'],
                    'course_url': chunk['course_url'],
                    'sequence': chunk['sequence'],
                    'categories': chunk['categories'],
                    'metadata': chunk['metadata']
                }
            )
            points.append(point)
        
        qdrant_client.upload_points(
            collection_name=collection_name,
            points=points,
            batch_size=30
        )
