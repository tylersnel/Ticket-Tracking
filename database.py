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
    def db_create_ticket(self, query1, query2, unit_name, action_type, sm_last_name, action_status, action_creator, comment):
        self.mydb.autocommit = True
        cursor = self.mydb.cursor()
        cursor.execute(query1, (unit_name, action_type, sm_last_name, action_status, action_creator))
        action_id = cursor.lastrowid
        cursor.execute(query2,(comment, action_id, action_creator))#adding comment, new action_id  and action_creator to comments table
        cursor.close()
        return action_id
    def db_assign_ticket(self, query1, action_id, assigned_tech_id, action_status): ## probaby can get rid of this
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
    def db_action_edit(self, query, unit_name, action_type, sm_last_name, assigned_tech_id, action_status, action_id):
        self.mydb.autocommit = True
        cursor=self.mydb.cursor()
        cursor.execute(query, (unit_name, action_type, sm_last_name, assigned_tech_id, action_status, action_id))
        result = cursor.rowcount
        cursor.close()
        return result
    #Fuction for search 
    #Returns search result
    def db_search(self, query, unit_name, action_type, sm_last_name, assigned_tech_id, action_status, action_creator):
        cursor=self.mydb.cursor()
        cursor.execute(query, (unit_name, action_type, sm_last_name, assigned_tech_id, action_status, action_creator))
        result= cursor.fetchall()
        cursor.close
        return result
    #Function used to search for actions by id
    #Used in the edit_action template
    def db_action_search(self, query, action_id):
        cursor=self.mydb.cursor()
        cursor.execute(query, (action_id,))
        result=cursor.fetchall()
        cursor.close
        return result
    #Function used for assigning an action
    def db_assign_action(self, query1, query2, query3, query4):
        cursor=self.mydb.cursor()
        cursor.execute(query1, (query2, query3, query4))
        result = cursor.rowcount
        cursor.close()
        return result
    #Function used to upload files to DB
    def db_upload_files(self, query, action_id, file_name, file_data, mime_type, user_id):
        cursor=self.mydb.cursor()
        cursor.execute(query, (action_id, file_name, file_data, mime_type, user_id))
        cursor.close()
        return True
        