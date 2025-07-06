from server.config.database import DbConnection

class BlockedKeywordsRepo:
    def add_keyword(self, keyword):
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT IGNORE INTO blocked_keywords (keyword) VALUES (%s)", (keyword,))
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": f"Keyword: {keyword} blocked."}

    def remove_keyword(self, keyword):
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM blocked_keywords WHERE keyword = %s", (keyword,))
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": f"Keyword: {keyword} unblocked."}

    def get_all_blocked_keywords(self):
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT keyword FROM blocked_keywords")
        keywords = [row["keyword"] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return keywords