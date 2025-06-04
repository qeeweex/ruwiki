import sqlite3
import hashlib
from article import Article, User


class Database:
    db_path = "database.db"
    schema_path = "schema.sql"

    @staticmethod
    def execute(sql_code: str, params: tuple = ()):
        conn = sqlite3.connect(Database.db_path)
        cursor = conn.cursor()
        if params:
            cursor.execute(sql_code, params)  # Используем execute для параметров
        else:
            cursor.executescript(sql_code)    # executescript для DDL-запросов
        conn.commit()
        conn.close()

    @staticmethod
    def create_tables():
        with open(Database.schema_path) as schema_file:
            sql_code = schema_file.read()
            Database.execute(sql_code)

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
    def find_user_by_id(user_id: int) -> User | None:
        users = Database.fetchall('SELECT * FROM users WHERE id = ?', [user_id])

        if not users:
            return None
        
        id, user_name, email, password_hash = users[0]
        return User(name=user_name, email=email)

    @staticmethod
    def find_article_by_id(article_id: int) -> Article | None:
        articles = Database.fetchall("SELECT * FROM articles WHERE id = ?", [article_id])

        if not articles: # if len(articles) == 0
            return None

        id, title, content, image, author_id = articles[0]
        author = Database.find_user_by_id(author_id)
        article = Article(id=id, title=title, content=content, image=image, author=author)

        return article

    @staticmethod
    def save(article: Article) -> bool:
        if Database.find_article_by_title(article.title) is not None:
            return False

        author_id = Database.find_user_id_by_name_or_email(article.author.email)
        Database.execute(f"""
        INSERT INTO articles (title, content, filename, author_id) VALUES (?, ?, ?, ?)
        """, (article.title, article.content, article.image, author_id))
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

        for (id, title, content, image, author_id) in Database.fetchall(
                "SELECT * FROM articles"):
            author = Database.find_user_by_id(author_id)
            articles.append(
                Article(
                    title=title,
                    content=content,
                    image=image,
                    id=id,
                    author=author,
                )
            )

        return articles
            
    @staticmethod
    def find_article_by_title(title: str):
        articles = Database.fetchall(
            "SELECT * FROM articles WHERE title = ?", [title])
        
        if not articles:
            return None
        
        id, title, content, image, author_id = articles[0]
        author = Database.find_user_by_id(author_id)
        return Article(
            title = title, 
            content = content, 
            image = image, 
            id = id, 
            author = author
        )
    
    @staticmethod
    def register_user(user_name, email, password):
        
        users = Database.fetchall("SELECT * FROM users WHERE user_name = ? OR email = ?", [user_name, email])
        
        print(users)

        if users:
            return False
        
        password_hash = hashlib.md5(password.encode()).hexdigest()
        
        Database.execute("INSERT INTO users (user_name, email, password_hash) "
                          "VALUES(?, ?, ?)",
                        [user_name, email, password_hash])
        
        return True

    
    @staticmethod
    def count_users():
        # т.к fetchall возвращает список с кортежом
        count = Database.fetchall("SELECT COUNT(*) FROM users")[0][0]
        return count
        
    @staticmethod
    def can_be_logged_in(user_or_email: str, password: str):
        users = Database.fetchall("SELECT * FROM users WHERE user_name = ? OR email = ? ", [user_or_email, password])

        if not users:
            return False
        
        user = users[0]
        real_password_hash = user[3]

        password_hash = hashlib.md5( password.encode() ).hexdigest()

        if real_password_hash != password_hash:
            return False
        return True
    
    @staticmethod
    def find_user_id_by_name_or_email(username_on_email):
        users = Database.fetchall("SELECT id FROM users WHERE user_name = ? OR email = ? ", [username_on_email, username_on_email])

        if not users:
            return None
        
        id = users[0][0]
        return id 