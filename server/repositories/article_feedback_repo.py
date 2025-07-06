from server.config.database import DbConnection

class ArticleFeedbackRepository:

    def __save_feedback(self, user_id: int, article_id: int, feedback_type: str):
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT feedback_type FROM user_article_feedback
            WHERE user_id = %s AND article_id = %s
            """,
            (user_id, article_id)
        )
        existing = cursor.fetchone()

        if existing:
            if existing["feedback_type"] != feedback_type:
                cursor.execute(
                    """
                    UPDATE user_article_feedback
                    SET feedback_type = %s
                    WHERE user_id = %s AND article_id = %s
                    """,
                    (feedback_type, user_id, article_id)
                )
                conn.commit()
                message = f"Feedback updated to '{feedback_type}' for Article ID {article_id}"
            else:
                message = f"No change. Already marked as '{feedback_type}' for Article ID {article_id}"
        else:
            cursor.execute(
                """
                INSERT INTO user_article_feedback(user_id, article_id, feedback_type)
                VALUES (%s, %s, %s)
                """,
                (user_id, article_id, feedback_type)
            )
            conn.commit()
            message = f"Feedback '{feedback_type}' added for Article ID {article_id}"

        cursor.close()
        conn.close()
        return {"message": message}

    def like_article_by_user(self, user_id: int, article_id: int):
        return self.__save_feedback(user_id, article_id, "like")

    def dislike_article_by_user(self, user_id: int, article_id: int):
        return self.__save_feedback(user_id, article_id, "dislike")
