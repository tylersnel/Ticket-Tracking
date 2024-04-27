import customtkinter
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="users"
)
cursor = db.cursor()
db.autocommit = True


""" customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("500x350") """
cursor.execute("CREATE TABLE IF NOT EXISTS Employees (id INT PRIMARY KEY, username VARCHAR(255), password VARCHAR(255))")

def create_user():
    user_name=input("Please enter username: ")
    password=input("Please enter password: ")
    query= "INSERT INTO Employees (username, password) VALUES (%s, %s)"

    cursor.execute(query, (user_name, password))

create_user()

""" frame=customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)
label = customtkinter.CTkLabel(master=frame, text="Login System", font=("Robot", 24))
label.pack(pady=12, padx=10)

button = customtkinter.CTkButton(master=frame, text="Login", command=login)
button.pack(pady=12, padx=10)

root.mainloop() """