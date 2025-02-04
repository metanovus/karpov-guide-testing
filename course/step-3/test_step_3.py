import pytest
from functions_step_3 import split_text


def test_text_shorter_than_min_length():
    text = "This is a short text."
    result = split_text(text, piece_size=1500, min_length=2000)
    assert result == [text], "Ошибка: вашей функции текст не должен быть разбит, если его длина меньше минимальной."


def test_text_exactly_min_length():
    text = "a" * 2000  # Текст точно минимальной длины
    result = split_text(text, piece_size=1500, min_length=2000)
    assert result == [text], "Ошибка: в вашей функции текст не должен быть разбит, если его длина точно равна минимальной."


def test_text_longer_than_min_length_but_not_splitted():
    text = "a" * 1999  # Текст длиной чуть меньше 2000 символов, не должен быть разделен
    result = split_text(text, piece_size=1500, min_length=2000)
    assert result == [text], "Ошибка: в вашей функции текст не должен быть разбит, если его длина меньше минимальной."


def test_text_split_into_pieces():
    text = "Здесь указан очень длинный текст. " * 200  # Текст длиной больше 2000, должен быть разбит на несколько частей
    print(len(text))
    result = split_text(text, piece_size=1500, min_length=2000)
    assert len(result) > 1, "Ошибка: в вашей функции текст должен быть разбит на несколько частей."


def test_text_with_sentences_split_correctly():
    text = "Предложение 1. Предложение 2. Предложение 3. Предложение 4." * 10  # Длинный текст с несколькими предложениями
    result = split_text(text, piece_size=100, min_length=400)
    assert len(result) > 1, "Ошибка: в вашей функции текст должен быть разбит на несколько частей."


def test_text_with_edge_case_pieace_size():
    text = "a" * 10  # Текст, который легко вмещается в один фрагмент
    result = split_text(text, piece_size=100, min_length=50)
    assert len(result) == 1, "Ошибка: в вашей функции текст должен вмещаться в один фрагмент, если его длина меньше размера фрагмента."
    
    text = "a" * 2000  # Длинный текст, который должен быть разбит
    result = split_text(text, piece_size=200, min_length=50)
    assert len(result) > 1, "Ошибка: в вашей функции текст должен быть разбит на несколько частей, если его длина превышает размер фрагмента."
