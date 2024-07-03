import flask
from flask import Flask, render_template, request
import os
import database

object = database.DB()
app = flask.Flask(__name__)

@app.route('/', methods=["GET"])
def main():
    return render_template("login.j2")

@app.route('/login', methods=["GET"])
def login():
    if request.method == "GET":
        user_name=request.args.get("user_name")
        password=request.args.get("password")

        query= "SELECT * from Employees WHERE username = %s AND password = %s"

        user = object.db_signin(query, user_name, password)
    
        if user[0][3] == 2: #if user is employee
            query2 = "SELECT * from Actions WHERE assigned_tech_id is NULL"
            unassigned_actions = object.db_query(query2)
            return render_template("employee_home.j2", user=user, unassigned_actions=unassigned_actions)
        else:
            print("Incorrect username or password. Try again")


@app.route('/employees', methods=["POST", "GET"])
def employees():
     query= "SELECT * from Employees"
     results = object.db_query(query)

     if results:
         return render_template("main.j2", employees=results )
         

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(port=port) 