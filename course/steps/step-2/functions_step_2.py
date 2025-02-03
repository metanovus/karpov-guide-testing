import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Tuple, Set
import re


def parse_titles(urls: List[str]) -> List[str]:
    """
    Парсит названия курса с заданных URL.

    Параметры:
    - urls (List[str]): Список URL-адресов для парсинга.

    Возвращаемое значение:
    - courses_titles (List[str]): Список названий курсов, извлеченных с сайтов.
    """
    courses_titles = []

    for url in urls:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Ошибка при загрузке страницы: {response.status_code}")
            continue

        soup = BeautifulSoup(response.text, 'html.parser')

        course_title = soup.find('h1', class_="tn-atom")
        course_title = re.split(r'\=|\||\.', course_title.text)[0].strip().replace(' ', ' ').replace(':', '')
        courses_titles.append(course_title)

        print(f'Найдена вакансия "{course_title}" с сайта: {url}')

    return sorted(courses_titles)
    

def parse_faq(urls: List[str]) -> Tuple[Dict[str, List[str]], List[str]]:
    """
    Парсит информацию о FAQ курсов с заданных URL.

    Если FAQ отсутствует, выводится соответствующее сообщение. Также добавляется обработка случая, когда необходимо "показать еще" для загрузки полного FAQ.

    Параметры:
    - urls (List[str]): Список URL-адресов для парсинга.

    Возвращаемое значение:
    - faq_collection (Dict[str, List[str]]): Словарь, где ключ — URL, а значение — список вопросов и ответов.
    """
    faq_collection = {}

    for url in urls:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Ошибка при загрузке страницы: {response.status_code}")
            continue

        soup = BeautifulSoup(response.text, 'html.parser')

        # Проверяем наличие FAQ
        if not any(elem.text.startswith('FAQ') for elem in soup.find_all('h2', class_='tn-atom')):
            print(f'FAQ с {url} не был загружен по причине его отсутствия!')
            continue

        # Получаем элементы FAQ
        elements_descr = soup.find_all('div', class_='t849')
        if any(elem.text.strip() == 'Показать еще' for elem in soup.find_all('button', type='button')):
            elements_descr = elements_descr[-2:]
        else:
            elements_descr = elements_descr[-1:]

        # Извлекаем вопросы и ответы
        result = re.split(r'\s{2,}', ''.join(e.text for e in elements_descr).replace('\xa0', ' '))[1:-1]
        questions_answers = [f'Вопрос: {result[i]}\nОтвет: {result[i + 1]}' for i in range(0, len(result), 2)]

        faq_collection[url] = questions_answers
        print(f'FAQ с {url} загружен успешно!')

    return faq_collection
    
    
def parse_information(urls: List[str]) -> Dict[str, List[str]]:
    """
    Парсит информацию о курсах с заданных URL. Извлекает текстовые блоки с информацией о курсе,
    удаляя лишние символы и форматируя текст в абзацы.

    Параметры:
    - urls (List[str]): Список URL-адресов для парсинга.

    Возвращаемое значение:
    - courses_information (Dict[str, List[str]]): Словарь, где ключ — URL, а значение — список текстовых блоков с информацией о курсе.

    Пример:
    >>> urls = ["http://example.com/course1", "http://example.com/course2"]
    >>> courses_information = parse_courses_information(urls)
    >>> print(courses_information)
    """
    info_collection = {}

    for url in urls:
        response = requests.get(url)
        if response.status_code != 200:
            print(f'Ошибка при загрузке страницы {url}')
            continue

        soup = BeautifulSoup(response.text, 'html.parser')
        result = soup.find_all('div', class_='tn-atom', field=re.compile('tn_text_\d+'))

        sequence, ready_res = '', []
        for elem in result:
            text = elem.text.strip()
            if text:
                sequence += text.translate({160: ' ', 65279: ' ', 10145: ' '}).replace('\u2009', '').replace('1. 2. 3. 4. 5.', '') + ' '
            else:
                ready_res.append(sequence)
                sequence = ''

        info_collection[url] = [res.strip() for res in ready_res if len(res) > 250]

        # если вышло, что у нас всего один абзац, и ничего не добавилось в информацию о курсе
        if not info_collection[url]:
            info_collection[url] = [sequence]

        print(f'Информация с {url} загружена успешно.')

    return info_collection
