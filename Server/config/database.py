import mysql.connector as sql
class DbConnection:

    @staticmethod
    def get_db_connection():
        try:
            # Establish connection
            conn = sql.connect(
                host="localhost",
                user="root",
                passwd="Amrit@1235",          # Your correct password
                database="news_aggregation_project",
                use_pure= True
            )
            return conn


            # # Execute SELECT query
            # cursor.execute("SELECT * FROM employees;")
            # rows = cursor.fetchall()
            # # Print each row
            # for row in rows:
            #     print(row)

        except sql.Error as err:
            print(f"MySQL Error: {err}")

# finally:
#     if cursor:
#         cursor.close()
#     if conn:
#         conn.close()
