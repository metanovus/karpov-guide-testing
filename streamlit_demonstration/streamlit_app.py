import streamlit as st
from langchain_mistralai.chat_models import ChatMistralAI
from langchain.memory import ConversationSummaryMemory
from langchain.chains import ConversationChain
from app.rag_utils import create_rag_prompt
from streamlit_chat import message


# Основная функция общения с моделью
def start_messaging(rag_top_k=5, max_memory_size=4096):
    # Настраиваем LLM
    llm = ChatMistralAI(
        model="mistral-small-latest",
        api_key='Rwfanxaxljkr1MRPcb0L9ogDf0e81zQf',
        streaming=True
    )

    conversation = ConversationChain(
        llm=llm,
        memory=ConversationSummaryMemory(llm=llm),
        verbose=True
    )

    # Инициализация переменных
    if "memory_size" not in st.session_state:
        st.session_state.memory_size = 0
    if "context_documents" not in st.session_state:
        st.session_state.context_documents = []
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Заголовок
    st.title("Чат с умным советником - karpov-guide 💬")

    # Кнопка для очистки чата
    if st.button("Очистить чат"):
        st.session_state.messages = []
        st.session_state.memory_size = 0
        st.session_state.context_documents = []
        st.rerun()

    # Отображение истории сообщений
    for i, message_data in enumerate(st.session_state.messages):
        if message_data['role'] == 'user':
            message(
                message_data['text'],
                is_user=True,
                key=f"user_{i}",
                avatar_style="thumbs",
                seed=i,
            )
        else:
            message(
                message_data['text'],
                is_user=False,
                key=f"model_{i}",
                avatar_style="bottts",
                seed=i,
            )

    def clear_text():
        st.session_state.user_input = st.session_state.widget
        st.session_state.widget = ""  # Очистить поле ввода

    # Поле ввода сообщения
    with st.form(key="chat_form"):
        user_input = st.text_input(
            "Введите сообщение",
            placeholder="Например, какие курсы подходят для аналитиков данных?",
            key="user_input",
            on_change=clear_text
        )
        submitted = st.form_submit_button("Отправить")

    if submitted and user_input:
        # Устанавливаем значение для session_state
        st.text_input("Введите сообщение", value="", key="user_input")
        
        # Сохраняем сообщение пользователя
        st.session_state.messages.append({"role": "user", "text": user_input})

        # Создаём RAG-подсказку
        prompt = create_rag_prompt(user_input, top_k=rag_top_k)

        # Загружаем новую память
        new_memory = conversation.memory.load_memory_variables({})['history']
        new_memory_size = len(new_memory)

        # Проверяем лимит памяти
        if st.session_state.memory_size + new_memory_size <= max_memory_size:
            st.session_state.context_documents.append(new_memory)
            st.session_state.memory_size += new_memory_size
            response = conversation.predict(input=prompt)
        else:
            st.warning("Достигнут предел памяти, дальнейшее накопление прекращено.")
            response = conversation.predict(input=user_input)

        # Сохраняем ответ модели
        st.session_state.messages.append({"role": "bot", "text": response})

        # Перезагружаем интерфейс, очищая поле ввода
        st.rerun()


# Запуск Streamlit
if __name__ == "__main__":
    start_messaging(rag_top_k=10)
