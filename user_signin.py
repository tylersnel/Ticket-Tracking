# working on sql table actions
import database

object = database.DB()

'''
Function that process user login
Makes call to database.py to see if username and password are correct
Returns: Array with user id and user permissions
'''
def signin():
    user_name=input("username: ")
    password=input("password: ")
    
    query= "SELECT * from Employees WHERE username = %s AND password = %s"

    result = object.db_signin(query, user_name, password)
    
    if result:
        for i in result:
            print("Welcome " + i[1])
            return [i[0], i[3]]
    else:
        print("Incorrect username or password. Try again")

