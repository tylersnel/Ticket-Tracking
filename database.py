import mysql.connector
class DB:
    def __del__(self):
        self.mydb.close()

    def __init__(self):
        self.mydb=mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="users"
        )
        print("Started DB connection")

    def db_query(self, query):
        cursor=self.mydb.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return result
        cursor.close()