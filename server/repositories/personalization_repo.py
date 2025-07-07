from server.config.database import DbConnection

class PersonalizationRepo:
    def get_user_category_counts(self, user_id):
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT c.category_name, SUM(cnt) as total_count
            FROM (
                SELECT acm.category_id, COUNT(*) as cnt
                FROM user_article_feedback ap
                JOIN article_category_mapping acm ON ap.article_id = acm.article_id
                WHERE ap.user_id = %s
                GROUP BY acm.category_id

                UNION ALL

                SELECT acm.category_id, COUNT(*) as cnt
                FROM read_history rh
                JOIN article_category_mapping acm ON rh.article_id = acm.article_id
                WHERE rh.user_id = %s
                GROUP BY acm.category_id

                UNION ALL

                SELECT acm.category_id, COUNT(*) as cnt
                FROM saved_article sa
                JOIN article_category_mapping acm ON sa.article_id = acm.article_id
                WHERE sa.user_id = %s
                GROUP BY acm.category_id

                UNION ALL

                SELECT np.category_id, COUNT(*) as cnt
                FROM user_notification_setting np
                WHERE np.user_id = %s AND np.is_enabled = TRUE
                GROUP BY np.category_id
            ) as all_cats
            JOIN category c ON all_cats.category_id = c.category_id
            GROUP BY c.category_name
            ORDER BY total_count DESC;
        """, (user_id, user_id, user_id, user_id))
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return {row['category_name']: row['total_count'] for row in result}
