from Server.config.database import DbConnection

class ExternalServerRepository:
    def fetch_all_external_servers(self):
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM external_server")
        servers = cursor.fetchall()

        cursor.close()
        conn.close()
        return servers
