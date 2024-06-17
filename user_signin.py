# working on sql table actions
import database

object = database.DB()

def signin():
    user_name=input("username: ")
    password=input("password: ")
    
    query= "SELECT * from Employees WHERE username = %s AND password = %s"

    result = object.db_signin(query, user_name, password)
    
    if result:
        for i in result:
            print("Welcome " + i[1])
            return i[0]
    else:
        print("Incorrect username or password. Try again")

