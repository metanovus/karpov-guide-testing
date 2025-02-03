from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer


# Инициализация Qdrant
qdrant_client = QdrantClient(
    url="https://e4a0270f-59cd-453d-9577-e33637c4ec29.us-east4-0.gcp.cloud.qdrant.io",
    api_key="gBVNUkVt2u7Mr-z5NcJnO4OX5gV2a6ztLW7nDvNrMupS5Mez1kNpZw"
)

model = SentenceTransformer('DeepPavlov/rubert-base-cased-sentence')


def search_similar(query, top_k=5):
    query_embedding = model.encode(query)
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


def create_rag_prompt(query, top_k=5):
    base_prompt = f"""Роль: ты — помощник по курсам Karpov.courses. Твоя задача - ненавязчиво и дружелюбно помочь пользователю с вопросами о курсах, используя только предоставленную информацию.

    Вопрос пользователя: {query}

    Контекст из базы знаний (отсортирован по релевантности):
    """

    end_prompt = """
        На основе предоставленной информации, пожалуйста:
        1. Дай подробный ответ на вопрос пользователя
        2. Укажи конкретные курсы, которые могут быть релевантны запросу
        3. Предоставь ссылки на рекомендуемые курсы

        ПРИ НАЛИЧИИ (если такой информации нет - НЕ ПИШИ НИЧЕГО, а если пользователь просит - ВЕДИ ЕГО НА ССЫЛКУ КУРСА):
        1. Информация об оплате курса
        2. Данные о преподаваемых технологиях
        3. Дата начала курса и его длительность

        Важно: 
        - Используй ТОЛЬКО русский язык при ответе на вопрос пользователя
        - Старайся использовать информацию из контекста
        - Если информации недостаточно, скажи пользователю перейти на сайт https://karpov.courses/ или в телеграм-канале https://t.me/+fPqRCFmZS9ZkZDZi
        - Не придумывай факты
        - Если у тебя нет какой-то информации в контексте, не пиши это пользователю, вежливо попроси его перейти на сайт с курсом или на главный сайт
        - Всегда указывай источник информации (название курса)"""

    results = search_similar(query, top_k=top_k)

    for result in results:

        if 'question' in result[1].payload:
            context_piece = f"""
            [FAQ] Курс: {result[1].payload['course_name']} (ссылка: {result[1].payload['course_url']})
            В: {result[1].payload['question']}
            О: {result[1].payload['answer']}
            """
        else:
            context_piece = f"""
            [Описание] Курс: {result[1].payload['course_name']} (ссылка: {result[1].payload['course_url']})
            {result[1].payload.get('sequence', '')}"""

        base_prompt += context_piece

    ready_prompt = base_prompt + end_prompt

    return ready_prompt