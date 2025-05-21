import hashlib
import sqlite3
from article import Article


class Database:
    db_path = "database.db"
    schema_path = "schema.sql"

    @staticmethod
    def execute(sql_code: str, params: tuple = ()):
        conn = sqlite3.connect(Database.db_path)
        
        cursor = conn.cursor()
        cursor.execute(sql_code, params)

        conn.commit()

    @staticmethod
    def create_tables():
        with open(Database.schema_path) as schema_file:
            sql_code = schema_file.read()
            conn = sqlite3.connect(Database.db_path)

            cursor = conn.cursor()
            cursor.executescript(sql_code)

            conn.commit()
            

    @staticmethod
    def update(article_id: int, title: str, content: str, image: str) -> bool:
        # Если статьи с таким id нет, ничего не делаем и возвращаем False
        if Database.find_article_by_id(article_id) is None:
            return False
        
        Database.execute(
            """
            UPDATE articles
            SET title = ?,
                content = ?,
                filename = ?
            WHERE id = ?
            """,
            [title, content, image, article_id]
        )
        return True

    @staticmethod
    def delete(article_id: int) -> bool:
        # Если статьи с таким id нет, ничего не делаем и возвращаем False
        if Database.find_article_by_id(article_id) is None:
            return False

        Database.execute("DELETE FROM articles WHERE id = ?", [article_id])
        return True

    @staticmethod
    def find_article_by_id(article_id: int) -> Article | None:
        articles = Database.fetchall("SELECT * FROM articles WHERE id = ?", [article_id])

        if not articles: # if len(articles) == 0
            return None

        id, title, content, image = articles[0]
        article = Article(id=id, title=title, content=content, image=image)

        return article

    @staticmethod
    def save(article: Article) -> bool:
        if Database.find_article_by_title(article.title) is not None:
            return False

        Database.execute(f"""
        INSERT INTO articles (title, content, filename) VALUES (?, ?, ?)
        """, (article.title, article.content, article.image))
        return True

    @staticmethod
    def fetchall(sql_code: str, params: tuple = ()):
        conn = sqlite3.connect(Database.db_path)
        
        cursor = conn.cursor()
        cursor.execute(sql_code, params)

        return cursor.fetchall()

    @staticmethod
    def get_all_articles():
        articles = []

        for (id, title, content, image) in Database.fetchall(
                "SELECT * FROM articles"):
            articles.append(
                Article(
                    title=title,
                    content=content,
                    image=image,
                    id=id
                )
            )

        return articles
            
    @staticmethod
    def find_article_by_title(title: str):
        articles = Database.fetchall(
            "SELECT * FROM articles WHERE title = ?", [title])
        
        if not articles:
            return None
        
        id, title, content, image = articles[0]
        return Article(title, content, image, id)

    @staticmethod
    def register_user(user_name, email, password):
        # 1. Узнать , если ли пользователи у который указан такой 
        # никнейм или почта      
        users = Database.fetchall(
            "SELECT * FROM users WHERE user_name = ? OR email = ?",
            [user_name, email]
        )
        if users:
            return False
        
        # 2. Получиться хэш от пароля, добавить пользователя в БД
        password_hash = hashlib.md5(password.encode()).hexdigest()
        Database.execute(
            "INSERT INTO users(user_name, email, password_hash) "
            "VALUES(?, ?, ?)",
            [user_name, email, password]
        )
        return True