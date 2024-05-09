
import database

object = database.DB()
object.autocommit = True

#object.db_query("CREATE TABLE IF NOT EXISTS Employees (id INT PRIMARY KEY, username VARCHAR(255), password VARCHAR(255))")

def create_user():
    user_name=input("Please enter username: ")
    password=input("Please enter password: ")
    query= "INSERT INTO Employees (username, password) VALUES (%s, %s)"

    if object.db_insert_new_user(query, user_name, password):
        print("User Succesfully Added")


