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
        self.set_isolation_level()
        print("Started DB connection")
    #Sets isolation level to see changes committed by other transactions
    def set_isolation_level(self):
        cursor = self.mydb.cursor()
        cursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED")
        cursor.close()
    #Function to run basic queries that don't have user input
    def db_query(self, query):
        cursor=self.mydb.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result
    #Function for created new user
    #Queries are the query, username, password, permissions    
    def db_insert_new_user(self, query1, query2, query3, query4):
        self.mydb.autocommit =  True
        cursor = self.mydb.cursor()
        cursor.execute(query1, (query2, query3, query4))
        return True
    #Function used for signing in a user
    def db_signin(self, query1, query2, query3):
        cursor=self.mydb.cursor()
        cursor.execute(query1, (query2, query3))
        result = cursor.fetchall()
        cursor.close()
        return result
    #Function for creating a new work ticket
    def db_create_ticket(self, query1, unit_name, action_type, sm_last_name, action_status, action_creator):
        self.mydb.autocommit = True
        cursor = self.mydb.cursor()
        cursor.execute(query1, (unit_name, action_type, sm_last_name, action_status, action_creator))
        cursor.close()
        return True
    def db_assign_ticket(self, query1, action_id, assigned_tech_id, action_status):
        self.mydb.autocommit = True
        cursor = self.mydb.cursor()
        cursor.execute(query1, (action_id, assigned_tech_id, action_status))
        #To check if DB was updated
        result = cursor.rowcount
        cursor.close()
        return result
    #Fucntion for fetching actions assigned to an employee
    #Queries are the actual query, user ID
    def db_assigned_actions_query(self, query1, query2):
        cursor=self.mydb.cursor()
        cursor.execute(query1, (query2,))
        result = cursor.fetchall()
        cursor.close()
        return result
     #Function used for ticket edits
     #Returns row count
    def db_ticket_edit(self, query1, query2, query3):
        self.mydb.autocommit = True
        cursor=self.mydb.cursor()
        cursor.execute(query1, (query2, query3))
        result = cursor.rowcount
        cursor.close()
        return result


        