from typing import List
import re


def split_text(text: str, piece_size: int = 1500, min_length: int = 2000) -> List[str]:
    """
    Разбивает длинный текст на меньшие части, каждая из которых не превышает заданный размер. 
    Если текст короче минимальной длины, возвращает его целиком.

    Параметры:
    - text (str): Исходный текст, который необходимо разделить на фрагменты.
    - piece_size (int): Максимальная длина каждого фрагмента (по умолчанию 1500 символов).
    - min_length (int): Минимальная длина текста, при которой он не будет разделен на фрагменты (по умолчанию 2000 символов).

    Возвращаемое значение:
    - List[str]: Список частей текста. Каждая часть — это строка текста длиной не более `piece_size` символов.
    """
    if len(text) <= min_length:
        return [text]

    text_pieces = []
    current_piece = ""

    sentences = re.split(r'(?<=\.) ', text)

    for sentence in sentences:
        if len(current_piece) + len(sentence) + 1 <= piece_size:
            current_piece += sentence + " "
        else:
            text_pieces.append(current_piece.strip())
            current_piece = sentence + " "

    if current_piece:
        text_pieces.append(current_piece.strip())

    return text_pieces
