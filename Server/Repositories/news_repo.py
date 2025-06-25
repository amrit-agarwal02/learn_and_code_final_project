from Server.config.database import DbConnection
from Server.schemas.news import NewsArticleCreate, NewsArticle

class NewsRepository:
    def save(self, news: NewsArticleCreate):
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO articles (server_id, title, description, content, source, url, published_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                news.server_id,
                news.title,
                news.description,
                news.content,
                news.source,
                news.url,
                news.published_at
            )
        )
        conn.commit()
        cursor.close()
        conn.close()
        return cursor.lastrowid



    def get_recent_news(self, count_of_recent_news: int):
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor(dictionary=True)  # Return results as dicts
        cursor.execute(
            """
            SELECT article_id, server_id, title, description, content, source, url, published_at
            FROM articles
            ORDER BY article_id DESC
            LIMIT %s
            """,
            (count_of_recent_news,)
        )
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        latest_news_article = [NewsArticle(**row) for row in rows]

        return latest_news_article

    def get_last_article_id(self):
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor()
        last_article_id = cursor.lastrowid

        return last_article_id

    def get_today_news(self):
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor(dictionary=True)  # Return results as dicts
        cursor.execute(
            """
            SELECT title, description, content, source, url, published_at FROM articles where 
            day(published_at) = day(curdate());
            """
        )
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        return rows

