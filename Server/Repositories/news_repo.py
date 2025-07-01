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
        cursor = conn.cursor(dictionary=True)
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

    def get_news_by_date_range(self, start_date, end_date, category_id):
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            f"""
            select title, description, content, source, url, published_at from articles t1 join article_category_mapping t2 
            on t1.article_id = t2.article_id  
            where date(published_at)>="{start_date}" and date(published_at)<="{end_date}"
            and category_id = {category_id};
            """
        )
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    def get_news_by_keyword(self, keyword):
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            f"""
                    select title, description, content, source, url, published_at from articles 
                    where concat_ws(' ',title,description, content) 
                    like "%{keyword}%";
            """
        )
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    def save_news_article_for_user(self, user_id, article_id):
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO saved_article (user_id, article_id)
            VALUES (%s, %s)
            """,
            (
                user_id,
                article_id
            )
        )
        conn.commit()
        cursor.close()
        conn.close()
        return cursor.lastrowid

    def get_saved_articles_for_user(self, user_id):
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT t1.article_id, t2.title, t2.description, t2.content, t2.url 
        from saved_article t1 join articles t2 on t1.article_id = t2.article_id
        where t1.user_id = %s;
        """
        cursor.execute(query,(user_id,))
        saved_articles = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return saved_articles

    def delete_saved_articles_for_user(self, user_id,article_id):
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
        DELETE from saved_article 
        where user_id = %s and article_id = %s;
        """
        cursor.execute(query,(user_id,article_id))
        deleted_rows = cursor.rowcount
        conn.commit()
        cursor.close()
        conn.close()
        return {"deleted": f"{deleted_rows} saved articles"}