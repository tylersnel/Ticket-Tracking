#This seems to work
import database

object = database.DB()

def signin():
    user_name=input("username: ")
    password=input("password: ")
    
    query= "SELECT * from Employees WHERE username = %s"

    result = object.db_signin(query, user_name)
    
    if result:
        for i in result:
            print(i)

signin()