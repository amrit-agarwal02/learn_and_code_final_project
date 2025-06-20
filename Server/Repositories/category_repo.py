from Server.config.database import DbConnection
from typing import List, Optional


class CategoryRepository:
    def get_all(self) -> List[dict]:
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM category ORDER BY category_id")
        categories = cursor.fetchall()
        cursor.close()
        conn.close()
        return categories

    def get_by_id(self, category_id: int) -> Optional[dict]:
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM category WHERE category_id = %s", (category_id,))
        category = cursor.fetchone()
        cursor.close()
        conn.close()
        return category

    def get_id_by_name(self, name: str) -> Optional[dict]:
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT category_id FROM category WHERE category_name = %s", (name,))
        category_id = cursor.fetchone()
        cursor.close()
        conn.close()
        return category_id

    def get_by_name(self, name: str) -> Optional[dict]:
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM category WHERE category_name = %s", (name,))
        category_id = cursor.fetchone()
        cursor.close()
        conn.close()
        return category_id

    def create(self, name: str, description: str = None) -> dict:
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO category (category_name) VALUES (%s)",
            (name,)
        )
        conn.commit()
        cursor.close()
        conn.close()

    def update(self, category_id: int, name: str = None, description: str = None) -> Optional[dict]:
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor()

        update_fields = []
        values = []

        if name is not None:
            update_fields.append("name = %s")
            values.append(name)

        if description is not None:
            update_fields.append("description = %s")
            values.append(description)

        if update_fields:
            values.append(category_id)
            query = f"UPDATE category SET {', '.join(update_fields)} WHERE category_id = %s"
            cursor.execute(query, values)
            conn.commit()

        cursor.close()
        conn.close()
        return self.get_by_id(category_id)

    def delete(self, category_id: int) -> bool:
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM category WHERE category_id = %s", (category_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True

    def insert_article_category(self, category_id, article_id):
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("insert into article_category_mapping(category_id, article_id) values(%s,%s)",(category_id, article_id))
        conn.commit()
        cursor.close()
        conn.close()

obj = CategoryRepository()

print(obj.get_all())
