"""
Used to assign a work ticket to an employee.
"""
import database

object = database.DB()

def assign_ticket(assigned_tech_id, action_id):
    result = None
    action_status="assigned"
    while not result:
        query = "UPDATE actions SET assigned_tech_id = %s, action_status = %s WHERE action_id = %s"


        result = object.db_assign_ticket(query, assigned_tech_id, action_status, action_id)
        if result==1:
            print("You have been assigned action number "+ action_id)
        else:
            action_id=input("Incorrect action ID number. Try again: ")

def change_status(action_id, action_status):
    result=None

    while not result:
        query = "UPDATE actions SET action_status = %s WHERE action_id = %s"


        result = object.db_ticket_edit(query, action_status, action_id)
        if result==1:
            print("Status updated for  "+ action_id)
        else:
            action_id=input("Incorrect action ID number. Try again: ")


