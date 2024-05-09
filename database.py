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
        cursor.close()
        return result
        
    def db_insert_new_user(self, query1, query2, query3):
        self.mydb.autocommit =  True
        cursor = self.mydb.cursor()
        cursor.execute(query1, (query2, query3))
        return True

    def db_signin(self, query1, query2):
        cursor=self.mydb.cursor()
        cursor.execute(query1, (query2,))
        result = cursor.fetchall()
        cursor.close()
        return result

        


        