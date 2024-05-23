"""File that is used to SQL queires so that user inputs are separated from DB queries
to help prevent injection attacks"""
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
    #Function to run basic queries that don't have user input
    def db_query(self, query):
        cursor=self.mydb.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result
    #Function for created new user    
    def db_insert_new_user(self, query1, query2, query3):
        self.mydb.autocommit =  True
        cursor = self.mydb.cursor()
        cursor.execute(query1, (query2, query3))
        return True
    #Function used for signing in a user
    def db_signin(self, query1, query2, query3):
        cursor=self.mydb.cursor()
        cursor.execute(query1, (query2, query3))
        result = cursor.fetchall()
        cursor.close()
        return result

        


        