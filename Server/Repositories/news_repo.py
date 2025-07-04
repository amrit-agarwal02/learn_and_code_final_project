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
            SELECT title, description, content, source, url, published_at, c.category_name 
            FROM articles a
            JOIN article_category_mapping acm ON a.article_id = acm.article_id
            JOIN category c ON acm.category_id = c.category_id 
            where day(published_at) = day(curdate())
            AND c.is_visible = TRUE
            AND a.is_visible = TRUE;
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
            select title, description, content, source, url, published_at, c.category_name
            FROM articles a
            JOIN article_category_mapping acm ON a.article_id = acm.article_id
            JOIN category c ON acm.category_id = c.category_id  
            where date(published_at)>="{start_date}" and date(published_at)<="{end_date}"
            and c.category_id = {category_id}
            AND c.is_visible = TRUE
            AND a.is_visible = TRUE;
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
                    select title, description, content, source, url, published_at, c.category_name
                    FROM articles a
                    JOIN article_category_mapping acm ON a.article_id = acm.article_id
                    JOIN category c ON acm.category_id = c.category_id 
                    where 
                    c.is_visible = TRUE
                    AND a.is_visible = TRUE
                    AND concat_ws(' ',title,description, content) 
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

    def insert_report(self, article_id, user_id, reason):
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT IGNORE INTO reports (article_id, user_id, reason)
            VALUES (%s, %s, %s)
        """, (article_id, user_id, reason))
        conn.commit()
        cursor.close()
        conn.close()

    def get_report_count(self, article_id):
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM reports WHERE article_id = %s
        """, (article_id,))
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return count

    def hide_article(self, article_id):
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE articles SET is_visible = FALSE WHERE article_id = %s
        """, (article_id,))
        conn.commit()
        cursor.close()
        conn.close()

        return {"Blocked": f"Article id {article_id} blocked for users"}

    def get_reported_articles(self):
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT article_id, count(*) as reported_count
            from reports 
            group by article_id
            order by reported_count
        """)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results

    def get_article_by_id(self, article_id: int):
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
                    Select title, description, content, source, url, published_at 
                    FROM articles a
                    JOIN article_category_mapping acm ON a.article_id = acm.article_id
                    JOIN category c ON acm.category_id = c.category_id 
                    where
                    a.article_id = %s
                    AND c.is_visible = TRUE
                    AND a.is_visible = TRUE
                    """
        cursor.execute(query, (article_id,))
        article = cursor.fetchone()
        cursor.close()
        return article

    def mark_article_as_read(self, user_id: int, article_id: int):
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        insert_query = "INSERT INTO read_history (user_id, article_id) VALUES (%s, %s);"
        cursor.execute(insert_query, (user_id, article_id))
        conn.commit()
        cursor.close()
        return {"Read": f"Article id {article_id} marked as read"}