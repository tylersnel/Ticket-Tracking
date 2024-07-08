import flask
from flask import Flask, render_template, request, redirect, url_for, session
import os
import database
from key import key

object = database.DB()
app = flask.Flask(__name__)
app.secret_key = key

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
        #for failed login attempt
        if not user:            
            return render_template("login.j2", login_error=True)

        elif user[0][3] == 2: #if user is employee
            ##### Maybe make this into one function? #####
            query2 = "SELECT * from Actions WHERE assigned_tech_id is NULL"
            unassigned_actions = object.db_query(query2)
            action_status='complete'
            query3 = "SELECT * from actions WHERE assigned_tech_id = %s AND action_status !=%s"
            #using the db_signin in fuction so not to have duplicate queries
            assigned_actions =  object.db_signin(query3, user[0][0], action_status)
            session['username']=user_name
            session['tech_id']=user[0][0]
            return render_template("employee_home.j2", user=user_name, tech_id=user[0][0], unassigned_actions=unassigned_actions, assigned_actions=assigned_actions)

@app.route('/edit_action/<int:action_id>', methods=["POST", "GET"])
def edit_action(action_id):
    if request.method == "GET":
        query = "SELECT * from Actions WHERE action_id = %s"
        action = object.db_action_search(query, action_id)
        return render_template("edit_action.j2", action=action, )
    elif request.method == "POST":
        #if the edit button is clicked
        if request.form.get("Edit_Action"):
            a_id = request.form["action_id"]
            unit = request.form["unit"]
            a_type = request.form["action_type"]
            last_name = request.form["sm_last_name"]
            tech_id = request.form["assigned_tech_id"]
            status = request.form["action_status"]
            if status == "Unassigned":
                tech_id = None #also unassigning tech_id
            query2 = "UPDATE actions SET unit_name = %s, action_type = %s, sm_last_name = %s, assigned_tech_id = %s, action_status = %s WHERE action_id = %s"
            result = object.db_action_edit(query2, unit, a_type, last_name, tech_id, status, a_id)
            
            if result:
                query2 = "SELECT * from Actions WHERE assigned_tech_id is NULL"
                unassigned_actions = object.db_query(query2)
                action_status='complete'
                query3 = "SELECT * from actions WHERE assigned_tech_id = %s AND action_status !=%s"
                #using the db_signin in fuction so not to have duplicate queries
                assigned_actions =  object.db_signin(query3, session['tech_id'], action_status)
                user=session['username']
                tech_id=session['tech_id']
                return render_template("employee_home.j2", user=user, tech_id=tech_id, unassigned_actions=unassigned_actions, assigned_actions=assigned_actions)
        
@app.route('/assign_action/<int:tech_id>/<int:action_id>', methods=["POST", "GET"])
def assign_action(tech_id, action_id):
    if request.method == "POST":
        if request.form.get("assign"):
            action_status= "Assigned"
            query = "UPDATE actions SET assigned_tech_id = %s, action_status = %s  WHERE action_id = %s"
            result = object.db_assign_action(query, tech_id, action_status, action_id)
        
            if result:
                    query2 = "SELECT * from Actions WHERE assigned_tech_id is NULL"
                    unassigned_actions = object.db_query(query2)
                    action_status='complete'
                    query3 = "SELECT * from actions WHERE assigned_tech_id = %s AND action_status !=%s"
                    #using the db_signin in fuction so not to have duplicate queries
                    assigned_actions =  object.db_signin(query3, tech_id, action_status)
                    user=session['username']
                    return render_template("employee_home.j2", user=user, tech_id=tech_id, unassigned_actions=unassigned_actions, assigned_actions=assigned_actions)
            else:
                print("Failed")
                return render_template("login.j2")

@app.route('/employees', methods=["POST", "GET"])
def employees():
     query= "SELECT * from Employees"
     results = object.db_query(query)

     if results:
         return render_template("main.j2", employees=results )
         

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(port=port) 