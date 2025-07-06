import mysql.connector as sql
class DbConnection:

    @staticmethod
    def get_db_connection():
        try:
            conn = sql.connect(
                host="localhost",
                user="root",
                passwd="Amrit@1235",          # Your correct password
                database="news_aggregation_project",
                use_pure= True
            )
            return conn
        except sql.Error as err:
            print(f"MySQL Error: {err}")

