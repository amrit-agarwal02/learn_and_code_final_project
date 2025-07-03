from unicodedata import category

from Server.config.database import DbConnection
from Server.Repositories.category_repo import CategoryRepository
from Server.Repositories.news_repo import NewsRepository
from Server.schemas.notification import NotificationSettingUpdate


class NotificationRepository:

    def __init__(self):
        self.news_repo = NewsRepository()
        self.category_repo = CategoryRepository()

    def save(self, user_id: int, category_id: int, keyword):
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            INSERT INTO user_notification_setting (user_id, category_id, keyword)
            VALUES (%s, %s, %s)
            """,
            (
                user_id,
                category_id,
                keyword
            )
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {
            "Notification Setting Stored Successfully"
        }

    def get_notification_settings(self, user):
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT * FROM user_notification_setting where 
            user_id = %s;
            """,
            (user["user_id"],)
        )
        rows = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()

        return rows

    def update_notification_setting(self, user_id, setting_id, notification_setting: NotificationSettingUpdate):
        category_id = self.category_repo.get_id_by_name(notification_setting.category)['category_id']
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
                UPDATE user_notification_setting 
                SET category_id = %s, is_enabled = %s, keyword = %s
                WHERE setting_id = %s AND user_id = %s
            """, (category_id, notification_setting.is_enabled, notification_setting.keyword, setting_id, user_id))
        conn.commit()
        cursor.close()
        conn.close()

        return {
            "Prefrence updated successfully"
        }

    def store_notifications(self):
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            INSERT IGNORE INTO notifications (user_id, article_id, message)
            SELECT t1.user_id, t3.article_id, t3.title
            FROM user_notification_setting t1
            JOIN article_category_mapping t2 ON t1.category_id = t2.category_id
            JOIN articles t3 ON t3.article_id = t2.article_id
            WHERE 
            (t1.keyword IS NULL OR 
            CONCAT_WS(' ', t3.title, t3.description, t3.content) LIKE CONCAT('%', t1.keyword, '%'))
            AND t3.fetched_at >= NOW() - INTERVAL 4 HOUR;
            """
        cursor.execute(query)
        inserted_rows = cursor.rowcount
        conn.commit()
        cursor.close()
        conn.close()
        return {
            "inserted_notifications": inserted_rows
        }

    def get_unread_notifications_grouped_by_user(self):
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
         SELECT u.email, u.user_id, 
        GROUP_CONCAT(CONCAT('Title - ', n.message, '\nURL   - ', a.url, '\n') SEPARATOR '\n') AS messages
        FROM notifications n
        JOIN users u ON u.user_id = n.user_id
        JOIN articles a ON a.article_id = n.article_id
        WHERE n.is_read = 0
        GROUP BY u.user_id;
        """)
        results = cursor.fetchall()

        cursor.close()
        conn.close()
        return results

    def get_unread_notifications_by_user(self, user_id):
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
        SELECT *
        FROM notifications n
        JOIN users u ON u.user_id = n.user_id
        JOIN articles a ON a.article_id = n.article_id
        WHERE n.is_read = 0
        and u.user_id = %s
        """,(user_id,))
        results = cursor.fetchall()

        cursor.close()
        conn.close()
        return results