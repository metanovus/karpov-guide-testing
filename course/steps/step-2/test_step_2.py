import pytest
from functions_step_2 import parse_titles, parse_faq, parse_information
    

real_courses_list = [
 'Визуализация данных и продвинутое Tableau',
 'Аналитика больших данных',
 'Hard Аналитика данных',
 'Симулятор A/B-тестов',
 'DOCKER С НУЛЯ',
 'Инженер данных с нуля',
 'ИНЖЕНЕР ДАННЫХ',
 'основы Python',
 'Гид по профессиям в Data Science',
 'Симулятор Data Science',
 'SYSTEM DESIGN',
 'Deep Learning Engineer',
 'Принятие решений на основе данных',
 'МАТЕМАТИКА ДЛЯ DATA SCIENCE',
 'СИМУЛЯТОР SQL',
 'Симулятор аналитика',
 'Аналитик данных',
 'ХАРДКОРНЫЙ MACHINE LEARNING',
 'Инженер машинного обучения',
 'ml engineering'
 ]
 
expected_count_of_faqs = {
'https://karpov.courses/analytics': 24,
'https://karpov.courses/data-driven': 9,
'https://karpov.courses/simulator-sql': 3,
'https://karpov.courses/mathsds': 7,
'https://karpov.courses/deep-learning': 6,
'https://karpov.courses/dataengineer-start': 12,
'https://karpov.courses/analytics-hard': 9,
'https://karpov.courses/pythonzero': 3,
'https://karpov.courses/big-data-analytics': 11,
'https://karpov.courses/simulator': 16,
'https://karpov.courses/simulator-ab': 11,
'https://karpov.courses/ml-engineering': 29,
'https://karpov.courses/ml-hard': 12,
'https://karpov.courses/simulator-ds': 6,
'https://karpov.courses/systemdesign': 8,
'https://karpov.courses/ml-start': 26,
'https://karpov.courses/dataengineer': 17
}

expected_count_of_info = {
 'https://karpov.courses/analytics': 8,
 'https://karpov.courses/analytics-hard': 4,
 'https://karpov.courses/big-data-analytics': 6,
 'https://karpov.courses/career/guide-ds': 1,
 'https://karpov.courses/data-driven': 7,
 'https://karpov.courses/dataengineer': 5,
 'https://karpov.courses/dataengineer-start': 6,
 'https://karpov.courses/datavisualization': 4,
 'https://karpov.courses/deep-learning': 5,
 'https://karpov.courses/docker': 1,
 'https://karpov.courses/mathsds': 2,
 'https://karpov.courses/ml-engineering': 4,
 'https://karpov.courses/ml-hard': 4,
 'https://karpov.courses/ml-start': 5,
 'https://karpov.courses/pythonzero': 1,
 'https://karpov.courses/simulator': 6,
 'https://karpov.courses/simulator-ab': 7,
 'https://karpov.courses/simulator-ds': 5,
 'https://karpov.courses/simulator-sql': 3,
 'https://karpov.courses/systemdesign': 2
}


urls = ['https://karpov.courses/analytics',
 'https://karpov.courses/analytics-hard',
 'https://karpov.courses/big-data-analytics',
 'https://karpov.courses/career/guide-ds',
 'https://karpov.courses/data-driven',
 'https://karpov.courses/dataengineer',
 'https://karpov.courses/dataengineer-start',
 'https://karpov.courses/datavisualization',
 'https://karpov.courses/deep-learning',
 'https://karpov.courses/docker',
 'https://karpov.courses/mathsds',
 'https://karpov.courses/ml-engineering',
 'https://karpov.courses/ml-hard',
 'https://karpov.courses/ml-start',
 'https://karpov.courses/pythonzero',
 'https://karpov.courses/simulator',
 'https://karpov.courses/simulator-ab',
 'https://karpov.courses/simulator-ds',
 'https://karpov.courses/simulator-sql',
 'https://karpov.courses/systemdesign']

@pytest.mark.parametrize("urls, expected_titles", [
    (urls, real_courses_list),
])
def test_parse_titles(urls, expected_titles):
    """
    Проверяет, что полученные названия курсов идентичны тем, что получил пользователь
    """
    try:
    	courses_titles = sorted([title.lower() for title in parse_titles(urls)])
    	assert courses_titles == sorted([title.lower() for title in expected_titles]), 'Возвращаемые значения не соответствуют требуемым' 
    except Exception as a:
    	print('Не удалось спарсить названия вакансий:', a)
    	
    	
@pytest.mark.parametrize("urls, expected_count_of_faqs", [
    (urls, expected_count_of_faqs),
])
def test_parse_faq(urls, expected_count_of_faqs):
    """
    Проверяет, что число абзацев FAQ соответствует тому, что спарсил пользователь
    """
    faq_collection = parse_faq(urls)
    faq_lengths = dict(sorted({key: len(faq_collection[key]) for key in faq_collection.keys()}.items(), key=lambda x: x[0]))
    assert expected_count_of_faqs == faq_lengths, 'Возвращаемые значения не соответствуют эталонным'
    
    
@pytest.mark.parametrize("urls, expected_count_of_info", [
    (urls, expected_count_of_info),
])
def test_parse_information(urls, expected_count_of_info):
    """
    Проверяет, что число абзацев основной информации соответствует тому, что спарсил пользователь
    """
    try:
        info_collection = parse_information(urls)
        info_lengths = dict(sorted({key: len(info_collection[key]) for key in info_collection.keys()}.items(), key=lambda x: x[0]))
        assert expected_count_of_info == info_lengths, 'Возвращаемые значения не соответствуют эталонным'
    except Exception as a:
        print('Не удалось спарсить данные:', a)
