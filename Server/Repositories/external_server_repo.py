from Server.config.database import DbConnection
from typing import Optional

class ExternalServerRepository:
    def fetch_all_external_servers(self):
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM external_server")
        servers = cursor.fetchall()

        cursor.close()
        conn.close()
        return servers

    def get_api_status(self):
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            select * from external_server
            """
        )
        external_server_data = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return external_server_data

    def get_server_by_id(self, server_id: int) -> Optional[dict]:
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM external_server WHERE server_id = %s", (server_id,))
        server = cursor.fetchone()
        cursor.close()
        conn.close()
        return server

    def update_server_api_key(self, server_id: int, new_api_key: str) -> dict:
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE external_server SET api_key = %s WHERE server_id = %s",
            (new_api_key, server_id)
        )
        conn.commit()
        updated = cursor.rowcount > 0
        cursor.close()
        conn.close()
        return {'API Key Updated Status ': "Success" if updated else "Failure"}

    def update_last_accessed(self, server_id: int):
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE external_server SET last_accessed = NOW() WHERE server_id = %s",
            (server_id,)
        )
        conn.commit()
        cursor.close()
        conn.close()

    def get_server_details(self):
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT server_name,api_key FROM external_server")
        server_details = cursor.fetchall()

        cursor.close()
        conn.close()
        return server_details
