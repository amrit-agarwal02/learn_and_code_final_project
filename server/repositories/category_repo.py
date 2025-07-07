import json
from server.config.database import DbConnection
from typing import List, Optional
from pathlib import Path

class CategoryRepository:

    def __init__(self):
        self.file_path = Path(__file__).parent.parent / "config" / "category_keywords.json"

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

    def create(self, name: str):
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO category (category_name) VALUES (%s)",
            (name,)
        )
        conn.commit()
        cursor.close()
        conn.close()

        return {"Category Successfully Created"}

    def insert_category_keywords(self,category_name: str, category_keywords: List[str]):
        self.categories = self.load_keywords()
        if category_name in self.categories:
            raise ValueError("Category Already Present")
        else:
            self.categories[category_name] = category_keywords
            self.save_keywords()


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

    def save_keywords(self):
        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump(self.categories, file, indent=2)

    def load_keywords(self):
        if not self.file_path.exists():
            return {}
        with self.file_path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def insert_article_category(self, category_id, article_id):
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("insert into article_category_mapping(category_id, article_id) values(%s,%s)",(category_id, article_id))
        conn.commit()
        cursor.close()
        conn.close()

    def hide_category(self, category_id):
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE categories SET is_visible = FALSE WHERE category_id = %s", (category_id,))
        conn.commit()
        cursor.close()
        conn.close()

    def update_visibility(self, category_id: int, is_visible: bool):
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE category SET is_visible = %s WHERE category_id = %s
        """, (is_visible, category_id))
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Category visibility updated"}
