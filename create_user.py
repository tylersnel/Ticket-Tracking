
import database

object = database.DB()
object.autocommit = True

#object.db_query("CREATE TABLE IF NOT EXISTS Employees (id INT PRIMARY KEY, username VARCHAR(255), password VARCHAR(255))")

def create_user():
    user_name=input("Please enter username: ")
    password=input("Please enter password: ")
    user_type=input("Are you an employee for the RPAC? Y or N ")
    user_type=user_type.lower()
    while user_type!= "y" and user_type!="n":
        user_type=input("Invalid input. Are you an employee for the RPAC? Y or N ")
        user_type=user_type.lower()
    
    permissions = 1 if user_type=='n' else 2

    query= "INSERT INTO Employees (username, password, permissions) VALUES (%s, %s, %s)"

    if object.db_insert_new_user(query, user_name, password, permissions):
        print("User Succesfully Added")
        # another query to return id of new user from DB
        
        query2 = "SELECT id FROM Employees WHERE username = %s AND password = %s "    
        user_id = object.db_signin(query2, user_name, password)
        for i in user_id:
            return [i[0], permissions]