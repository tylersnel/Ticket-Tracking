
import database

object = database.DB()

"""
Used by customers so that they can input work tickets. Customer must input unit name, action type and 
last name of the service member that the ticket is for.
"""

def create_ticket(user_id):
    unit_name=input("Please enter unit name: ")
    action_type=input("Please enter action type: ")
    sm_last_name=input("Please enter service member's last name: ")
    action_status="unassigned"
    query= "INSERT INTO actions (unit_name, action_type, sm_last_name, action_status, action_creator) VALUES (%s, %s, %s, %s, %s)"

    if object.db_create_ticket(query, unit_name, action_type, sm_last_name, action_status, user_id):
        print("Ticket Succesfully Added")


