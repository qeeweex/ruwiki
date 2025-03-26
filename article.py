from dataclasses import dataclass

@dataclass
class Article:
    title: str
    content: str
    image: str | None = None

def save_to_database():
    """Сохраняет статью в базу данных"""
    ...

def get_from_database():
    ...