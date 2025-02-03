import pandas as pd
from typing import List, Dict


def prepare_faq_chunks(faq_collection: Dict[str, List[str]], courses_df: pd.DataFrame, start_id: int = 0) -> List[Dict]:
    """
    Подготавливает чанки для FAQ, извлекая вопросы и ответы с добавлением метаданных для каждого чанка.

    Эта функция принимает коллекцию FAQ для каждого курса и соответствующую информацию о курсах, а затем разбивает
    каждый вопрос и ответ на отдельные чанки с добавлением метаданных, таких как идентификатор курса и индекс вопроса.

    Параметры:
    - faq_collection (Dict[str, List[str]]): Коллекция FAQ, где ключ — это URL курса, а значение — список строк в формате "Вопрос: <text> Ответ: <text>".
    - courses_df (pd.DataFrame): DataFrame, содержащий названия курсов и их URL.
    - start_id (int): Начальный индекс для нумерации чанков. По умолчанию равен 0.

    Возвращаемое значение:
    - List[Dict]: Список чанков, где каждый чанк представляет собой словарь с информацией о вопросах и ответах.
    """
    
    chunks = []
    
    course_names = dict(zip(courses_df['course_url'], courses_df['course_name']))
    
    for course_url, qa_pairs in faq_collection.items():
        course_name = course_names[course_url]
        
        for i, qa_pair in enumerate(qa_pairs, start=start_id):       
            chunk = {
                'chunk_id': f"{course_url.split('/')[-1]}_{i}",
                'course_name': course_name,
                'course_url': course_url,
                'question_and_answer': qa_pair,
                'metadata': {
                    'chunk_type': 'qa',
                    'course_id': course_url.split('/')[-1],
                    'qa_index': i,
                    'total_qa_pairs': len(qa_pairs)
                }
            }
            chunks.append(chunk)
    
    return chunks
    
    
def prepare_info_chunks(info_collection: Dict[str, List[Dict]], courses_df: pd.DataFrame, start_id: int = 0) -> List[Dict]:
    """
    Подготавливает чанки для основной информации о курсе, включая описание и категории.

    Эта функция принимает коллекцию информации о курсе и соответствующую информацию о курсах, затем разбивает
    данные на отдельные чанки, добавляя метаданные для каждого элемента, такие как идентификатор курса и индекс.

    Параметры:
    - info_collection (Dict[str, List[Dict]]): Коллекция информации о курсах, где ключ — это URL курса, а значение — список словарей с информацией (например, описание, категории).
    - courses_df (pd.DataFrame): DataFrame, содержащий названия курсов и их URL.
    - start_id (int): Начальный индекс для нумерации чанков. По умолчанию равен 0.

    Возвращаемое значение:
    - List[Dict]: Список чанков, где каждый чанк содержит информацию о курсе, включая описание и категории.
    """
    chunks = []
    
    course_names = dict(zip(courses_df['course_url'], courses_df['course_name']))

    for course_url, values in info_collection.items():
        course_name = course_names[course_url]

        for i, elem in enumerate(values, start=start_id):
            chunk = {
                'chunk_id': f"{course_url.split('/')[-1]}_{i}",
                'course_name': course_name,
                'course_url': course_url,
                'sequence': elem['sequence'],
                'categories': elem['categories'],
                'metadata': {
                    'chunk_type': 'course_information',
                    'course_id': course_url.split('/')[-1],
                    'course_information_index': i,
                    'total_sequences': len(values)
                }
            }
            chunks.append(chunk)
    
    return chunks
