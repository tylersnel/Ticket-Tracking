import flask
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
import os
import database
from key import key
import io
import mimetypes

object = database.DB()
app = flask.Flask(__name__)
app.secret_key = key

def render_home(user_name, tech_id):
    query2 = "SELECT * from Actions WHERE assigned_tech_id is NULL"
    unassigned_actions = object.db_query(query2)
    action_status='Assigned'
    query3 = "SELECT * from actions WHERE assigned_tech_id = %s AND action_status =%s"
    #using the db_signin in fuction so not to have duplicate queries
    assigned_actions =  object.db_signin(query3, tech_id, action_status)
    return render_template("employee_home.j2", user_name=user_name, tech_id=tech_id, unassigned_actions=unassigned_actions, assigned_actions=assigned_actions)   

@app.route('/', methods=["GET"])
def main():
    if 'username' in session:
        user_name=session['username']
        tech_id=session['tech_id']
        return render_home(user_name, tech_id)
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
            session['username']=user_name
            session['tech_id']=user[0][0]
            return redirect (url_for('main'))

@app.route('/edit_action/<int:action_id>', methods=["POST", "GET"])
def edit_action(action_id):
    if request.method == "GET":
        query = "SELECT * from Actions WHERE action_id = %s"
        action = object.db_action_search(query, action_id)
        query2 = "SELECT * from Comments WHERE action_id = %s"
        comments = object.db_action_search(query2, action_id) # Using db_action_search to not duplicate queries
        return render_template("edit_action.j2", action=action, comments=comments)
    elif request.method == "POST":
        #if the edit button is clicked
        if request.form.get("Edit_Action"):
            a_id = request.form["action_id"]
            unit = request.form["unit"]
            a_type = request.form["action_type"]
            last_name = request.form["sm_last_name"]
            tech_id = request.form["assigned_tech_id"]
            status = request.form["action_status"]
            new_comment = request.form["comment"]
            if status == "Unassigned":
                tech_id = None #also unassigning tech_id
            query2 = "UPDATE actions SET unit_name = %s, action_type = %s, sm_last_name = %s, assigned_tech_id = %s, action_status = %s WHERE action_id = %s"
            object.db_action_edit(query2, unit, a_type, last_name, tech_id, status, a_id)
            if new_comment !='':
                query3 = "INSERT INTO comments (comment, action_id, user_id) VALUES (%s, %s, %s)"
                object.db_assign_action(query3, new_comment,a_id,tech_id)
             
            return redirect (url_for('main'))
        
@app.route('/assign_action/<int:tech_id>/<int:action_id>', methods=["POST", "GET"])
def assign_action(tech_id, action_id):
    if request.method == "POST":
        if request.form.get("assign"):
            action_status= "Assigned"
            query = "UPDATE actions SET assigned_tech_id = %s, action_status = %s  WHERE action_id = %s"
            result = object.db_assign_action(query, tech_id, action_status, action_id)
        
            if result:
                    return redirect (url_for('main'))
            else:
                print("Failed")
                return render_template("login.j2")

@app.route('/create_action', methods=["POST", "GET"])
def create_action():
    if request.method == "POST":
        if request.form.get("Create_Action"):
            unit = request.form["unit"]
            action_type = request.form["action_type"]
            sm_last_name = request.form["sm_last_name"]
            action_status = "unassigned"
            action_creator = session['tech_id']
            comment= request.form["comments"]
            query = "INSERT INTO actions (unit_name, action_type, sm_last_name, action_status, action_creator) VALUES (%s, %s, %s, %s, %s)"
            query2 = "INSERT INTO comments(comment, action_id, user_id) VALUES (%s, %s, %s)"
            action_id = object.db_create_ticket(query, query2, unit, action_type, sm_last_name, action_status, action_creator, comment)
            
            if 'files' in request.files:
                print("hi")
                files = request.files.getlist('files')
                for file in files:
                    if file:
                        file_data = file.read()
                        file_name = file.filename
                        mime_type = file.mimetype
                        query3 = "INSERT INTO files (action_id, file_name, file_data, mime_type, user_id) VALUES (%s, %s, %s, %s, %s)"
                        object.db_upload_files(query3, action_id, file_name, file_data, mime_type, action_creator)
                flash("Action Created")        
                return redirect (url_for('main'))
            flash("Action Created")    
            return redirect (url_for('main'))

    return render_template("create_action.j2")

@app.route('/view_action/<int:action_id>', methods=["POST", "GET"])
def view_action(action_id):
    if request.method == "GET":
        query = "SELECT * from Actions WHERE action_id = %s"
        action = object.db_action_search(query, action_id)
        query2 = "SELECT * from Comments WHERE action_id = %s"
        comments = object.db_action_search(query2, action_id)
        query3 = "SELECT * from Files WHERE action_id = %s"
        files = object.db_action_search(query3, action_id)
        return render_template("view_action.j2", action=action, comments=comments, files=files)
    
@app.route('/download/<int:id>/<file_name>', methods=["POST", "GET"])
def file_download(id, file_name):
    if request.method == "GET":
        query = "SELECT * from Files WHERE id = %s"
        result = object.db_download_file(query, id)

        if result:
            file_data = result[3]
            mimetype = result[4]
            return send_file(io.BytesIO(file_data), download_name=file_name, mimetype=mimetype, as_attachment=True)
        return "File not found", 404


@app.route('/employees', methods=["POST", "GET"])
def employees():
     query= "SELECT * from Employees"
     results = object.db_query(query)

     if results:
         return render_template("main.j2", employees=results )
         

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(port=port) 