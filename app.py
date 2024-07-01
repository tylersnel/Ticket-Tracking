import flask
from flask import Flask, render_template
import os
import database

object = database.DB()
app = flask.Flask(__name__)

@app.route('/')
def home():
    pass

@app.route("/employees", methods=["POST", "GET"])
def employees():
     query= "SELECT * from Employees"
     results = object.db_query(query)

     if results:
         return render_template("main.j2", employees=results )
         

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(port=port) 