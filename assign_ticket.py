"""
Used to assign a work ticket to an employee.
"""
import database

object = database.DB()

def assign_ticket(assigned_tech_id, action_id):
    result = None
    while not result:
        query= "UPDATE actions SET assigned_tech_id = %s WHERE action_id = %s"

        result=object.db_assign_ticket(query, assigned_tech_id, action_id)
        if result==1:
            print("You have been assigned action number "+ action_id)
        else:
            action_id=input("Incorrect action ID number. Try again: ")