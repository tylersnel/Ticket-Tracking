"""
Used by customers so that they can input work tickets. Customer must input unit name, action type and 
last name of the service member that the ticket is for.
"""
import database

object = database.DB()

def create_ticket():
    unit_name=input("Please enter username: ")
    action_type=input("Please enter password: ")
    sm_last_name=input("Please enter service members last name: ")
    query= "INSERT INTO actions (unit_name, action_type, sm_last_name) VALUES (%s, %s, %s)"

    if object.db_create_ticket(query, unit_name, action_type, sm_last_name):
        print("Ticket Succesfully Added")

######Working on this section. Haven't tested it yet. Run test#########