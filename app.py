import flask
from flask import render_template, request, redirect, url_for, session, flash, send_file
import os
import sys
import sys
import database
from key import key
import io

object = database.DB()
app = flask.Flask(__name__)
app.secret_key = key


def render_employee_home(user_name, tech_id):
    #function used to allow for easier redirection back to home page for employees when coming from other pages
    query2 = "SELECT * from Actions WHERE assigned_tech_id is NULL"
    unassigned_actions = object.db_query(query2)
    action_status='Assigned'
    query3 = "SELECT * from actions WHERE assigned_tech_id = %s AND action_status =%s"
    #using the db_signin in fuction so not to have duplicate queries
    assigned_actions =  object.db_signin(query3, tech_id, action_status)
    return render_template("employee_home.j2", user_name=user_name, tech_id=tech_id, unassigned_actions=unassigned_actions, assigned_actions=assigned_actions)   

def render_customer_home(customer_id):
    #function used to allow for easier redirection back to home page for customerswhen coming from other pages
    #Uses db_signin funtion to reduce need of multiple functions
    
    #Gets actions created by current user
    action_status_assigned='Assigned'
    query = "SELECT * from actions WHERE action_creator= %s AND action_status =%s"
    assigned_actions = object.db_signin(query, customer_id, action_status_assigned)
    
    action_status_unassigned='unassigned'
    unassigned_actions = object.db_signin(query, customer_id, action_status_unassigned)

    action_status_rwo='RWO'
    rwo_actions = object.db_signin(query, customer_id,  action_status_rwo)

    return render_template("customer_home.j2", assigned_actions=assigned_actions, unassigned_actions=unassigned_actions, RWO_actions=rwo_actions)

#helper function to send variables to render home pages. Also helps with redirection back to home page when coming from other pages
@app.route('/', methods=["GET"])
def main():
    if session.get('username') != None:
        permissions = session['permissions']
        if permissions==2: #if employee
            user_name=session['username']
            tech_id=session['id']
            return render_employee_home(user_name, tech_id)
        elif permissions==1: #if customer
            customer_id=session['id']
            return render_customer_home(customer_id)
    return render_template("login.j2")

@app.route('/login', methods=["GET"])
def login():
    if request.method == "GET":
        user_name = request.args.get("user_name")
        password = request.args.get("password")

        # Using parameterized query to prevent SQL injection
        query = "SELECT * FROM Employees WHERE username = %s AND password = %s"
        user = object.db_signin(query, user_name, password)

        # For failed login attempt
        if not user:            
            return render_template("login.j2", login_error=True)

        session['username'] = user_name
        session['id'] = user[0][0]
        session['permissions'] = user[0][3]
        return redirect(url_for('main'))


@app.route('/edit_action/<int:action_id>', methods=["POST", "GET"])
def edit_action(action_id):
    if request.method == "GET":
        return handle_edit_get(action_id)
    elif request.method == "POST":
        return handle_edit_post(action_id)

def handle_edit_get(action_id):
        query = "SELECT * from Actions WHERE action_id = %s"
        action = object.db_action_search(query, action_id)
        query2 = "SELECT * from Comments WHERE action_id = %s"
        comments = object.db_action_search(query2, action_id) # Using db_action_search to not duplicate queries
        query3 = "SELECT * from Files WHERE action_id = %s"
        files = object.db_action_search(query3, action_id)
        return render_template("edit_action.j2", action=action, comments=comments, files=files)

def handle_file(action_id):
    files = request.files.getlist('files')
    for file in files:
         if file:
            file_data = file.read()
            file_name = file.filename
            mime_type = file.mimetype
            action_creator=session['id']
            query4 = "INSERT INTO files (action_id, file_name, file_data, mime_type, user_id) VALUES (%s, %s, %s, %s, %s)"
            object.db_upload_files(query4, action_id, file_name, file_data, mime_type, action_creator)

def handle_edit_post(action_id):
        if request.form.get("Edit_Action"):
            a_id = request.form["action_id"]
            unit = request.form["unit"]
            a_type = request.form["action_type"]
            last_name = request.form["sm_last_name"]
            tech_id = request.form["assigned_tech_id"]
            if not tech_id: # if there is no tech assinged yet. None allows the querey to execute because of FK
                tech_id = None
            status = request.form["action_status"]
            new_comment = request.form["comment"]
            if status == "Unassigned" or status == "RWO":
                tech_id = None #also unassigning tech_id if action is being returned so other techs can see it when action comes back
            query2 = "UPDATE actions SET unit_name = %s, action_type = %s, sm_last_name = %s, assigned_tech_id = %s, action_status = %s WHERE action_id = %s"
            object.db_action_edit(query2, unit, a_type, last_name, tech_id, status, a_id)
            if new_comment !='':
                commentor_id=session['id'] 
                query3 = "INSERT INTO comments (comment, action_id, user_id) VALUES (%s, %s, %s)"
                object.db_assign_action(query3, new_comment,a_id,commentor_id)
            
            if 'files' in request.files:
                handle_file(action_id)

            return redirect (url_for('main'))
        
@app.route('/assign_action/<int:tech_id>/<int:action_id>', methods=["POST", "GET"])
def assign_action(tech_id, action_id):
    if request.method == "POST" and request.form.get("assign"):
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
    if request.method == "POST" and request.form.get("Create_Action"):
        unit = request.form["unit"]
        action_type = request.form["action_type"]
        sm_last_name = request.form["sm_last_name"]
        action_status = "Unassigned"
        action_creator = session['id']
        comment= request.form["comments"]
        query = "INSERT INTO actions (unit_name, action_type, sm_last_name, action_status, action_creator) VALUES (%s, %s, %s, %s, %s)"
        query2 = "INSERT INTO comments(comment, action_id, user_id) VALUES (%s, %s, %s)"
        action_id = object.db_create_ticket(query, query2, unit, action_type, sm_last_name, action_status, action_creator, comment)
            
        if 'files' in request.files:
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
         
@app.route('/logout')
def logout():
    session['username']=None
    session['id']=None
    flash('You have successfully logged yourself out.')
    return render_template("login.j2")

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    if(False): 
        if os.fork() > 0:
            sys.exit()  # Exit the parent process
        os.setsid()  # Detach from terminal
        if os.fork() > 0:
            sys.exit()  # Exit the second parent process
        sys.stdout.flush()
        sys.stderr.flush()
    app.run(host="0.0.0.0",port=port) 
